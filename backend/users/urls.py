from django.urls import path
from .views import RegisterUserView, MeView, UserProfileView
from .auth_views import GoogleLoginView, SetUsernameView

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('me/', MeView.as_view()),
    path("profile/",  UserProfileView.as_view(), name="profile"),

    # Trades a Google ID token for this app's own JWT pair. Verified against
    # Google's public certificates, so no service account key is involved.
    path("google/", GoogleLoginView.as_view(), name="google_login"),
    path("username/", SetUsernameView.as_view(), name="set_username"),
]
