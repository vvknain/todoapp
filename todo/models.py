# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    pass

    class Admin:
        pass


class TodoList(models.Model):
    title = models.CharField(max_length=50)
    created_by = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    shared_with = models.ManyToManyField(User, related_name='+')
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["created"]


class Todo(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    todolist = models.ForeignKey(TodoList)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["created"]
