from django.contrib import admin

from .models import Track, MetaData


class TrackAdmin(admin.ModelAdmin):
    list_display = ('description', 'uploaded_at', 'raw_data')



# Register your models here.
admin.site.register(Track, TrackAdmin)
admin.site.register(MetaData)
