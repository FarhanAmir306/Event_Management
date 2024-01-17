from django.contrib import admin
from . import models


class category_admin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    list_display=['name','slug']

admin.site.register(models.Category,category_admin)
admin.site.register(models.Event)
admin.site.register(models.UpcomingEvent)


