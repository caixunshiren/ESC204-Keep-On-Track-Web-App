# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Track(models.Model):
    raw_data = models.FileField(upload_to='raw/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def display_track(self):
        ret = {
            'description': str(self.description),
            'timestamp': self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
            'file_url': self.raw_data.url,
        }
        return ret
