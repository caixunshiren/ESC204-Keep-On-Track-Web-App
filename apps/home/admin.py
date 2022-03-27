from django.contrib import admin

from .models import Track


class TrackAdmin(admin.ModelAdmin):
    list_display = ('description', 'uploaded_at', 'raw_data')



# Register your models here.
admin.site.register(Track, TrackAdmin)

