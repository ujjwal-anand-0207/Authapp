from django.urls import path, include
from account.views import UserRegistrationView , UserLoginView ,UserProfileView, UserChangePasswordView ,SendPasswordResetView
from account.views import UserPasswordResetView
urlpatterns = [
    path("register/", UserRegistrationView.as_view(),name="register"),
    path("login/", UserLoginView.as_view(),name="login"),
    path("profile/",UserProfileView.as_view(),name="profile"),
    path("changepassword/",UserChangePasswordView.as_view(),name="changepassword"),
    path('send-reset-password-email/',SendPasswordResetView.as_view(),name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name="reset-password")
]
