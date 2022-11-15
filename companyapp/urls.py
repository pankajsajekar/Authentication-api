from django.urls import path
from companyapp import views
from companyapp.views import EmployerRegisterView, EmployerLoginView
from jobportal.views import UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView


urlpatterns = [
    path('', views.register,  name=''),
    path('eregister/', EmployerRegisterView.as_view(), name='EmployerRegister'),
    path('elogin/', EmployerLoginView.as_view(), name='EmployerLogin'),
    path('echangepassword/', UserChangePasswordView.as_view(), name=''),
    path('eresetemail/', SendPasswordResetEmailView.as_view(), name=''),
    path('eresetpassword/', UserPasswordResetView.as_view(), name=''),
]