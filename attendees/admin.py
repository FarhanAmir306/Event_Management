from django.contrib import admin
from .models import Attendent,Event_Accept
# Register your models here.
class EventShow(admin.ModelAdmin):
    list_display=['name','event']

admin.site.register(Attendent)
admin.site.register(Event_Accept, EventShow)