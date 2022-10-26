from django.contrib import admin
from django.urls import path
from jobportal import views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('jobportal.urls'))
    # path('register-api/', views.register_api),
    # path('login-api/', views.login_api),
]
