from codecs import backslashreplace_errors
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify 
import uuid
import datetime

# Create your models here.

class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    allowed_users = models.ManyToManyField(User, default=User, blank=True, related_name='allowed_project_users')
    title = models.CharField(max_length=63)
    slug = models.SlugField(unique=True, default=uuid.uuid4)

    def __str__(self):
        return self.author.username + ": " + self.title

class ToDo(models.Model):
    title = models.CharField(max_length=63)
    description = models.TextField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_time = models.DateTimeField(null=True, blank=True)
    done = models.BooleanField(default=False)
    author = models.ForeignKey(User, default=User, on_delete=models.CASCADE, null=True)
    allowed_users = models.ManyToManyField(User, default=User, blank=True, related_name='allowed_users')
    priority_choices = [(1, "Priority 1"), (2, "Priority 2"), (3, "Priority 3"), (4, "Priority 4")]
    priority = models.CharField(max_length=1, choices=priority_choices, default=4)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    date_done = models.DateTimeField(default=None, null=True, blank=True)
 
    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, default=User, on_delete=models.CASCADE, null=True)
    task = models.ForeignKey(ToDo, default=ToDo, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.author.username + ": " + self.content

class Invite(models.Model):
    sender = models.ForeignKey(User, default=User, on_delete=models.CASCADE, null=True, blank=True, related_name='sender')
    reciever = models.ForeignKey(User, default=User, on_delete=models.CASCADE, null=True, blank=True, related_name='reciever')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="project_invite")
    accepted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.sender.username + " : " + self.reciever.username + " (" + self.project.title + ")"
