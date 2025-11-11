from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('invite/', views.InviteCreateView.as_view(), name='invite-create'),
    path('invitations/', views.ListInvitationsView.as_view(), name='invitationslist'),
    path('accept-invite/', views.AcceptInviteView.as_view(), name='acceptinvite'),
    path('me/', views.MeView.as_view(), name='me'),
    # JWT endpoints from Simple JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Password reset endpoints
    path("password-reset-request/", views.PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset-approve/<int:request_id>/", views.ApprovePasswordResetView.as_view(), name="password_reset_approve"),
    path("reset-password/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset-requests/", views.PasswordResetRequestListView.as_view(), name="password_reset_requests_list"),
]