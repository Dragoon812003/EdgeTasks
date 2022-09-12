# Generated by Django 4.1 on 2022-08-28 14:59

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_alter_invite_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_invite', to='main.project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='allowed_users',
            field=models.ManyToManyField(blank=True, default=django.contrib.auth.models.User, null=True, related_name='allowed_project_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
