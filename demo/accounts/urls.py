from django.conf.urls import url
from . import views

urlpatterns = [
    url("hello/", views.HelloView.as_view(), name="hello"),
    url("signup_api/", views.Signup.as_view(), name="signup_api"),
    url("login_api/", views.Login.as_view(), name="login_api"),
]
