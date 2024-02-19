from django.urls import path
from users.views import UserView, LoginView, LogoutView
# from .views import api_home


urlpatterns = [
    path("", UserView.as_view(), name="user"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]