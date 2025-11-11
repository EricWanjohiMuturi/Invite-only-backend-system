from rest_framework import serializers
from .models import CustomUser, Invitation, PasswordResetRequest
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role', 'first_name', 'last_name']
        read_only_fields = ['id', 'role']

class AdminUserCreateSerializer(serializers.ModelSerializer):
    # used by admins to create users directly (optional)
    class Meta:
        model = CustomUser
        fields = ['email', 'role', 'first_name', 'last_name']

class InvitationSerializer(serializers.ModelSerializer):
    invited_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Invitation
        fields = ['id', 'email', 'role', 'invited_by', 'created_at', 'expires_at', 'token', 'accepted']
        read_only_fields = ['id', 'token', 'created_at', 'invited_by', 'accepted']

class AcceptInviteSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_token(self, value):
        try:
            invite = Invitation.objects.get(token=value)
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invalid invitation token')
        if invite.accepted:
            raise serializers.ValidationError('This invitation has already been accepted')
        if invite.is_expired():
            raise serializers.ValidationError('This invitation has expired')
        return value

    def save(self):
        data = self.validated_data
        invite = Invitation.objects.get(token=data['token'])
        user = CustomUser.objects.create_user(
            email=invite.email,
            password=data['password'],
            first_name=data['first_name'],
            last_name=data.get('last_name', ''),
            role=invite.role,
        )
        invite.mark_accepted()
        return user
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email.")
        return value


class PasswordResetApproveSerializer(serializers.Serializer):
    token = serializers.UUIDField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(min_length=8)

class PasswordResetRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = PasswordResetRequest
        fields = ['id', 'user_email', 'approved', 'token', 'created_at', 'expires_at']