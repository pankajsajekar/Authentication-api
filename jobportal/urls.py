from django.urls import path
from jobportal.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView, UserLogoutView, AdminLoginView, UserView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    # path('login-api/', views.login_api),

    # Admin login
    path('admin/all_user/', UserView.as_view(), name='user_view'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login') 
]
