from django.urls import path
from .views import RegisterUserView, MeView, UserProfileView

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('me/', MeView.as_view()),
    path("profile/",  UserProfileView.as_view(), name="profile")
]
