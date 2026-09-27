"""Verifies Firebase Google sign-in tokens without any service account key.

A Firebase ID token is an ordinary RS256 JWT signed by Google. Verifying one
needs only Google's *public* signing certificates plus the project id, both of
which are public information - so this module needs no private credentials and
no firebase-admin dependency.

What that choice costs is written down here so it is not rediscovered later.
Because the backend holds no key, it cannot:

  * mint Firebase custom tokens, so a password-login user cannot be given a
    Firebase identity tied to their Django account; they sign in to Firebase
    anonymously instead, and their chat display name is self-reported.
  * write to the Realtime Database, so there is no server-maintained index of
    who belongs to which room. The database rules therefore admit any signed-in
    user who knows a room code, rather than only that room's participants.

If either of those matters later, the fix is a service account key plus the
membership index the rules would then check.
"""

import logging
import os
import threading
import time

import jwt
import requests
from cryptography.x509 import load_pem_x509_certificate

logger = logging.getLogger(__name__)

# Google publishes the certificates that sign Firebase ID tokens here. They
# rotate, so the response is cached for a while rather than per-request.
CERT_URL = (
    "https://www.googleapis.com/robot/v1/metadata/x509/"
    "securetoken@system.gserviceaccount.com"
)
CERT_CACHE_SECONDS = 3600
CERT_FETCH_TIMEOUT = 10

_cert_lock = threading.Lock()
_certs = {}
_certs_fetched_at = 0.0


class FirebaseNotConfigured(RuntimeError):
    """Raised when Google sign-in is used without FIREBASE_PROJECT_ID set."""


class FirebaseError(RuntimeError):
    """Raised when a token is present but could not be trusted."""


def project_id():
    return os.environ.get("FIREBASE_PROJECT_ID", "").strip()


def is_configured():
    """True when Google sign-in can be verified. One public value is enough."""
    return bool(project_id())


def _signing_keys(force_refresh=False):
    """Returns {kid: public key}, fetched from Google and cached in process."""
    global _certs, _certs_fetched_at

    with _cert_lock:
        fresh = (time.monotonic() - _certs_fetched_at) < CERT_CACHE_SECONDS
        if _certs and fresh and not force_refresh:
            return _certs

        try:
            response = requests.get(CERT_URL, timeout=CERT_FETCH_TIMEOUT)
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:
            # Serve a stale cache rather than lock everyone out over a blip.
            if _certs:
                logger.warning("Could not refresh Google's signing certificates "
                               "(%s); using the cached set.", exc)
                return _certs
            raise FirebaseError(
                f"Could not fetch Google's signing certificates: {exc}"
            ) from exc

        _certs = {
            kid: load_pem_x509_certificate(pem.encode()).public_key()
            for kid, pem in payload.items()
        }
        _certs_fetched_at = time.monotonic()
        return _certs


def verify_google_id_token(id_token):
    """Verifies a Firebase ID token and returns its claims.

    The token arrives from the browser, so it is attacker-controlled until
    every one of these has been checked: the signature against Google's
    current certificates, the audience (this project), the issuer, and expiry.
    PyJWT enforces aud/iss/exp; the signature needs the right key, which is
    selected by the token's own `kid` header.
    """
    if not is_configured():
        raise FirebaseNotConfigured(
            "FIREBASE_PROJECT_ID is not set, so Google sign-in cannot be verified."
        )

    pid = project_id()

    try:
        kid = jwt.get_unverified_header(id_token).get("kid")
    except Exception as exc:
        raise FirebaseError("That sign-in token is malformed.") from exc

    if not kid:
        raise FirebaseError("That sign-in token carries no key id.")

    keys = _signing_keys()
    if kid not in keys:
        # An unknown kid usually means the certificates have just rotated.
        keys = _signing_keys(force_refresh=True)
    key = keys.get(kid)
    if key is None:
        raise FirebaseError("That sign-in token was signed by an unknown key.")

    try:
        claims = jwt.decode(
            id_token,
            key=key,
            algorithms=["RS256"],
            audience=pid,
            issuer=f"https://securetoken.google.com/{pid}",
            options={"require": ["exp", "iat", "aud", "iss", "sub"]},
        )
    except jwt.ExpiredSignatureError as exc:
        raise FirebaseError("That sign-in has expired. Please try again.") from exc
    except jwt.InvalidTokenError as exc:
        raise FirebaseError(f"Could not verify Google sign-in: {exc}") from exc

    # `sub` is the Firebase uid. An empty one would mean a token we should not
    # be treating as an identity at all.
    if not claims.get("sub"):
        raise FirebaseError("That sign-in token identifies no user.")

    if not claims.get("email"):
        raise FirebaseError("That Google account did not supply an email address.")

    # An unverified address must not be able to claim an existing account, or
    # anyone could register someone else's email and take it over.
    if not claims.get("email_verified", False):
        raise FirebaseError("That Google account's email address is not verified.")

    return claims
