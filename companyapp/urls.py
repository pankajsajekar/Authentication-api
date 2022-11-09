from django.urls import path
from companyapp import views
from companyapp.views import EmployerRegisterView, EmployerLoginView

urlpatterns = [
    path('', views.register,  name=''),
    path('eregister/', EmployerRegisterView.as_view(), name='EmployerRegister'),
    path('elogin/', EmployerLoginView.as_view(), name='EmployerLogin')
]