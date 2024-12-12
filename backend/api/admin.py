from django.contrib import admin
from .models import Note, Course

# Register your models here.

admin.site.register(Note)
admin.site.register(Course)