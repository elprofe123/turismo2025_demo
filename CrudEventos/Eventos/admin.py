from django.contrib import admin
from .models import Evento
from django.contrib.admin.models import LogEntry
from django.contrib.admin import site 
# Register your models here.
admin.site.register(Evento)


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_time', 'content_type', 'object_repr', 'action_flag')
    list_filter = ('action_time', 'user', 'action_flag')
    search_fields = ('object_repr',)
site.register(LogEntry,LogEntryAdmin)