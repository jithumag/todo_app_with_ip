from django.contrib import admin
from .models import User,TodoItem


admin.site.register(User)
admin.site.register(TodoItem)