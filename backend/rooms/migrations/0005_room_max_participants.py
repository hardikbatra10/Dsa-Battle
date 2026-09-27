import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Adds Room.max_participants.

    Additive only. Autogeneration also wanted to narrow Room.id from
    BigAutoField to AutoField, which is the same pre-existing DEFAULT_AUTO_FIELD
    drift left out of the other migrations in this project.

    Rooms created before this field existed get MIN_PARTICIPANTS (3). That is
    the deliberate choice: any higher default could mark an already-populated
    room as needing more people than it will ever get.
    """

    dependencies = [
        ('rooms', '0004_alter_room_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='max_participants',
            field=models.IntegerField(
                default=3,
                validators=[
                    django.core.validators.MinValueValidator(3),
                    django.core.validators.MaxValueValidator(9),
                ],
            ),
        ),
    ]
