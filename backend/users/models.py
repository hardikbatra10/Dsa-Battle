from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    rating = models.IntegerField(default = 0)
    streak = models.IntegerField(default = 0)

    # False only while a Google-created account is still carrying the
    # placeholder username derived from its email address. Persisted rather
    # than inferred at sign-in, so refreshing the page mid-setup does not
    # lose the fact that the name was never actually chosen.
    #
    # Defaults to True: everyone who registered with the form picked their
    # own username, and so did every account that existed before this field.
    has_set_username = models.BooleanField(default = True)

