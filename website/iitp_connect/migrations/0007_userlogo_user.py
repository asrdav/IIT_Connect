# Generated by Django 2.1.2 on 2018-12-01 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iitp_connect', '0006_auto_20181201_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlogo',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]