from django.db import migrations, models


class Migration(migrations.Migration):
    """Adds Submission.counted.

    Deliberately additive only. Autogeneration also wanted to narrow
    Submission.id from BigAutoField to AutoField (bigint -> integer), which
    is an unrelated pre-existing drift caused by DEFAULT_AUTO_FIELD not being
    set in settings. Applying it would rewrite the table and shrink the id
    range for no benefit, so it is left out.

    Existing rows default to counted=True, which is correct: every submission
    made before this feature existed was made while its contest was running.
    """

    dependencies = [
        ('submissions', '0004_submission_failure_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='counted',
            field=models.BooleanField(default=True),
        ),
    ]
