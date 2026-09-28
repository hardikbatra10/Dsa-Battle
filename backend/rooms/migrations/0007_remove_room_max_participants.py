from django.db import migrations


class Migration(migrations.Migration):
    """Drops Room.max_participants again; rooms now take anyone with the code.

    Safe to apply in either order relative to a deploy. No code that has ever
    been deployed references this column: the capacity feature was only ever
    live on a development machine, and the currently released code inserts
    rooms without it. Dropping it therefore cannot break a running release,
    which is the opposite of the situation when it was added.

    The DEFAULT added in 0006 goes with the column.
    """

    dependencies = [
        ('rooms', '0006_room_max_participants_db_default'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='max_participants',
        ),
    ]
