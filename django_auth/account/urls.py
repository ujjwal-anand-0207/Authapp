from django.urls import path, include
from account.views import UserRegistrationView , UserLoginView ,UserProfileView
urlpatterns = [
    path("register/", UserRegistrationView.as_view(),name="register"),
    path("login/", UserLoginView.as_view(),name="login"),
    path("profile/",UserProfileView.as_view(),name="profile")
]
