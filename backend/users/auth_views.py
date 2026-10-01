"""Firebase-backed auth endpoints, kept separate from the plain CRUD views.

Both endpoints sit on the same principle: Firebase authenticates, Django
authorises. Nothing here lets a client influence which Django account it ends
up as beyond proving ownership of a verified Google email address.
"""

import logging

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .services.firebase import (
    FirebaseError,
    FirebaseNotConfigured,
    verify_google_id_token,
)

logger = logging.getLogger(__name__)
User = get_user_model()

# Django's username field permits letters, digits and @ . + - _ only, so a
# Google display name or email local-part has to be reduced to that set.
USERNAME_SAFE = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@.+-_"
)


def _placeholder_username(email):
    """A unique stand-in username for a brand new Google account.

    Only ever temporary: the account is flagged has_set_username=False and the
    client sends the user to pick a real one before they can do anything else.
    A value is still needed up front because username is unique and required.
    """
    base = "".join(c for c in email.split("@")[0] if c in USERNAME_SAFE)[:24]
    if not base:
        base = "player"

    candidate = base
    # An existing username is not an error here - two people can hold the same
    # local part on different domains - so keep suffixing until one is free.
    while User.objects.filter(username=candidate).exists():
        candidate = f"{base}_{get_random_string(4, '0123456789')}"[:30]
    return candidate


def _issue_jwt(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


class GoogleLoginView(APIView):
    """Exchanges a Firebase Google ID token for this app's own JWT pair.

    The account is matched on the verified email address, which is the only
    identifier Google guarantees. A user who originally registered with a
    password and later signs in with Google on the same address lands on their
    existing account rather than a duplicate.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        id_token = (request.data.get("id_token") or "").strip()
        if not id_token:
            return Response(
                {"error": "id_token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            claims = verify_google_id_token(id_token)
        except FirebaseNotConfigured as exc:
            logger.error("Google sign-in attempted while unconfigured: %s", exc)
            return Response(
                {"error": "Google sign-in is not configured on this server."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except FirebaseError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        email = claims["email"].lower()

        try:
            with transaction.atomic():
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        "username": _placeholder_username(email),
                        # The name was derived, not chosen. The client reads
                        # this back from the profile and routes them to pick
                        # one before anything else becomes reachable.
                        "has_set_username": False,
                    },
                )
                if created:
                    # No usable password: this account can only be entered
                    # through Google until its owner sets one.
                    user.set_unusable_password()
                    user.save(update_fields=["password"])
        except IntegrityError:
            # Two concurrent first-time sign-ins for the same address; the
            # loser of the race just reads the row the winner committed.
            user = User.objects.get(email=email)
            created = False

        if not user.is_active:
            return Response(
                {"error": "This account has been disabled."},
                status=status.HTTP_403_FORBIDDEN,
            )

        tokens = _issue_jwt(user)
        tokens["created"] = created
        return Response(tokens, status=status.HTTP_200_OK)



class SetUsernameView(APIView):
    """Lets a signed-in user claim their username.

    Deliberately not a general profile editor: it only runs while
    has_set_username is False, so this cannot be used to rename an established
    account out from under the leaderboards and submission history that
    display it.
    """

    permission_classes = [IsAuthenticated]

    MIN_LENGTH = 3
    MAX_LENGTH = 20
    ALLOWED = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    )

    def post(self, request):
        user = request.user

        if user.has_set_username:
            return Response(
                {"error": "Your username has already been set."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = (request.data.get("username") or "").strip()

        if len(username) < self.MIN_LENGTH or len(username) > self.MAX_LENGTH:
            return Response(
                {"error": f"Username must be {self.MIN_LENGTH}-{self.MAX_LENGTH} characters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not set(username) <= self.ALLOWED:
            return Response(
                {"error": "Use only letters, numbers and underscores."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Case-insensitive, so "Hardik" cannot shadow an existing "hardik" on
        # a leaderboard. Excludes self, though self still holds a placeholder.
        taken = User.objects.filter(username__iexact=username).exclude(id=user.id).exists()
        if taken:
            return Response(
                {"error": "That username is taken."},
                status=status.HTTP_409_CONFLICT,
            )

        user.username = username
        user.has_set_username = True
        try:
            user.save(update_fields=["username", "has_set_username"])
        except IntegrityError:
            # Someone claimed it between the check above and this write.
            return Response(
                {"error": "That username was just taken. Try another."},
                status=status.HTTP_409_CONFLICT,
            )

        return Response({"username": user.username}, status=status.HTTP_200_OK)
