import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Reset admin password"

    def handle(self, *args, **kwargs):

        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        user = User.objects.get(username=username)

        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS("Password updated successfully.")
        )