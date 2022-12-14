"""simplemrp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView

from . import admin as AccountAdmin
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('planning/', include('planning.urls')),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path('accounts/edit/', views.EditAccount.as_view(), name='edit_account'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]