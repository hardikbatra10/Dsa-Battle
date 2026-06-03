from django.urls import path
from .views import RegisterUserView, MeView

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('me/', MeView.as_view())
]
