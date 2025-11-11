from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Invitation, CustomUser, PasswordResetRequest
from .serializers import *
from .permissions import IsAdminOrDirector
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from drf_spectacular.utils import extend_schema
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .utils.email_utils import send_invitation_email, send_password_reset_email, send_admin_password_reset_request_email
from django.shortcuts import get_object_or_404

@extend_schema(
    summary="Invite a new user",
    description="Admins and Directors can invite new users by specifying their email and role. Sends an invitation email.",
    responses={
        201: InvitationSerializer,
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden"},
    },
    request=InvitationSerializer,
)
class InviteCreateView(generics.CreateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrDirector]

    def perform_create(self, serializer):
        expires_at = timezone.now() + timedelta(minutes=20)
        serializer.save(invited_by=self.request.user, expires_at=expires_at)
        invitation = serializer.instance

        # Send invitation email using Mailtrap API
        send_invitation_email(invitation, self.request)

        
class ListInvitationsView(generics.ListAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrDirector]

    def get_queryset(self):
        # admins see invites they sent; optionally all invites if you prefer
        return Invitation.objects.filter(invited_by=self.request.user)

@extend_schema(
    summary="Accept invitation",
    description="Accept an invitation using a valid token and set up the user account.",
    request=AcceptInviteSerializer,
    responses={201: UserSerializer, 400: {"description": "Invalid or expired token"}},
)
class AcceptInviteView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AcceptInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

@extend_schema(
    summary="List password reset requests",
    description="Admins can view all password reset requests submitted by users.",
    responses={
        200: PasswordResetRequestSerializer(many=True),
        403: {"description": "Forbidden"},
    },
)    
class PasswordResetRequestListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PasswordResetRequestSerializer

    def get_queryset(self):
        if self.request.user.role != "admin":
            return PasswordResetRequest.objects.none()
        return PasswordResetRequest.objects.all().order_by('-created_at')

@extend_schema(
    summary="Request password reset",
    description="Users can request a password reset. Notifies admins to approve the request.",
    request=InvitationSerializer,
    responses={
        201: {"description": "Password reset request submitted."},
        400: {"description": "Bad Request"},
        404: {"description": "User with this email not found."},
    },
)    
class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        user = get_object_or_404(CustomUser, email=email)

        # Create a reset request expiring in 20 minutes
        expires_at = timezone.now() + timedelta(minutes=20)
        PasswordResetRequest.objects.create(user=user, expires_at=expires_at)

        # Notify admins by email
        admin_emails = list(CustomUser.objects.filter(role="admin").values_list("email", flat=True))
        if admin_emails:
            send_admin_password_reset_request_email(admin_emails, user)

        return Response(
            {"detail": "Password reset request submitted. Await admin approval."},
            status=status.HTTP_201_CREATED
        )

@extend_schema(
    summary="Approve password reset request",
    description="Admins can approve password reset requests. Sends a password reset email with a secure link.",
    responses={
        200: {"description": "Password reset link sent successfully."},
        403: {"description": "Forbidden"},
        404: {"description": "Password reset request not found or already approved."},
    },
)    
class ApprovePasswordResetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, request_id):
        if request.user.role != "admin":
            return Response({"detail": "Only admins can approve password resets."}, status=status.HTTP_403_FORBIDDEN)

        reset_request = get_object_or_404(PasswordResetRequest, id=request_id, approved=False)
        reset_request.approved = True
        reset_request.save()

        #reset_url = f"{request.scheme}://{request.get_host()}/api/auth/reset-password/?token={reset_request.token}"
        reset_url = f"{self.request.scheme}://{self.request.get_host()}/api/auth/reset-password/?token={reset_request.token}"


        # 👇 Clean, readable call
        send_password_reset_email(
            user=reset_request.user,
            reset_url=reset_url,
            expires_at=reset_request.expires_at
        )

        return Response({"detail": "Password reset link sent successfully."}, status=status.HTTP_200_OK)

@extend_schema(
    summary="Confirm password reset",
    description="Users can reset their password using the token sent to their email.",
    request=PasswordResetConfirmSerializer,
    responses={
        200: {"description": "Password successfully reset."},
        400: {"description": "Invalid or expired token."},
    },
)
class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        reset_request = get_object_or_404(PasswordResetRequest, token=token, approved=True)

        if reset_request.is_expired():
            return Response({"detail": "Reset link has expired."}, status=status.HTTP_400_BAD_REQUEST)

        user = reset_request.user
        user.set_password(new_password)
        user.save()
        reset_request.delete()

        return Response({"detail": "Password successfully reset."}, status=status.HTTP_200_OK)