# Generated by Django 4.1 on 2022-08-17 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Acount_app', '0015_delete_notification'),
        ('Tutorial_app', '0012_alter_videotutorial_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videotutorial',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='video_tutorial', to='Acount_app.techer'),
            preserve_default=False,
        ),
    ]