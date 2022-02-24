from django.contrib import admin
from .models import Event, PatientCalendar

# Register your models here.
# admin.site.register(Event)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    ordering = ('date',)
    search_fields = ('title', 'date')
    list_filter = ('date', )


@admin.register(PatientCalendar)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', )

