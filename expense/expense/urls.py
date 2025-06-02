from django.contrib import admin
from django.urls import path, include
from Apps.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
    path("forgetpassword/", forgetpass, name="forgetpass"),
    
    path("__reload__/", include("django_browser_reload.urls")),
]
