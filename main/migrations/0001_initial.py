# Generated by Django 4.1 on 2022-08-28 14:46

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import main.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=63)),
                ('slug', models.SlugField(default=uuid.uuid4, unique=True)),
                ('allowed_users', models.ManyToManyField(blank=True, default=django.contrib.auth.models.User, related_name='allowed_project_users', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ToDo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63)),
                ('description', models.TextField(max_length=255)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_time', models.DateTimeField(blank=True, null=True)),
                ('done', models.BooleanField(default=False)),
                ('priority', models.CharField(choices=[(1, 'Priority 1'), (2, 'Priority 2'), (3, 'Priority 3'), (4, 'Priority 4')], default=4, max_length=1)),
                ('allowed_users', models.ManyToManyField(blank=True, default=django.contrib.auth.models.User, related_name='allowed_users', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.todo')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.project')),
            ],
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('project', models.ForeignKey(blank=True, default=main.models.Project, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_invite', to='main.project')),
                ('reciever', models.ForeignKey(blank=True, default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reciever', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('date', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(default=main.models.ToDo, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.todo')),
            ],
        ),
    ]
