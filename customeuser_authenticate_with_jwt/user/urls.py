from django.urls import path
from user.views import UserRegisterationView,UserLoginView,UserProfileView,UserChangePasswordView,UserSendResetPasswordEmailView,UserResetPasswordView

urlpatterns = [
    path('register/', UserRegisterationView.as_view(),name='registeration'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('user-profile/', UserProfileView.as_view(),name='profile'),
    path('user-change-password/', UserChangePasswordView.as_view(),name='UserChangePasswordView'),
    path('user-send-password-reset-email/', UserSendResetPasswordEmailView.as_view(),name='UserSendResetPasswordEmailView'),
    path('user-password-reset/<uid>/<token>/', UserResetPasswordView.as_view(),name='UserResetPasswordView'),
]