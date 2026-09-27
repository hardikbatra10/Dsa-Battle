from django.db import migrations


class Migration(migrations.Migration):
    """Keeps a database-level DEFAULT on Room.max_participants.

    Django adds a column with a default and then immediately drops it, because
    it treats defaults as an application concern. That is fine when code and
    schema ship together, but this project migrates a shared hosted database
    from a developer machine, so there is always a window where the running
    code predates the column. During that window every INSERT omits the column
    and fails the NOT NULL constraint - which took room creation down in
    production once already.

    Holding the default in the database closes that window: old code can still
    insert, and new code overrides it explicitly anyway. Purely additive, and
    reversible.
    """

    dependencies = [
        ('rooms', '0005_room_max_participants'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE rooms_room ALTER COLUMN max_participants SET DEFAULT 3;",
            reverse_sql="ALTER TABLE rooms_room ALTER COLUMN max_participants DROP DEFAULT;",
        ),
    ]
