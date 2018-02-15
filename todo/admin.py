# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Todo, TodoList, User


class TodolistAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created', 'modified')
    list_filter = ('created_by', 'created')
    search_fields = ('title',)


class TodoAdmin(admin.ModelAdmin):
    list_display = ('todolist', 'created', 'deadline')
    list_filter = ('created', 'todolist', 'deadline')
    search_fields = ('todolist',)


admin.site.register(Todo, TodoAdmin)
admin.site.register(TodoList, TodolistAdmin)
admin.site.register(User)

# Register your models here.
