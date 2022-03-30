# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Metadata
class MetaData(models.Model):
    total_clients = models.IntegerField(blank=True, default=0)
    total_time = models.FloatField(blank=True, default=0.0)
    total_distance = models.FloatField(blank=True, default=0.0)
    total_locations = models.FloatField(blank=True, default=0.0)

    def refresh(self):
        self.total_clients = Track.objects.count()
        # to be completed
        # self.total_time = Track.objects.count()
        # self.total_distance = Track.objects.count()
        # self.total_locations = Track.objects.count()
        self.save()

    def aggregate_coords(self):
        pass

    def file_loader(self, dir):
        pass

    def aggregated_export(self):
        print("aggregated_export")
        pass

    def display(self):
        return {
            'total_clients': "    "+str(self.total_clients),
            'total_time': "    "+str(self.total_time)+" hours",
            'total_distance': "    "+str(self.total_distance)+" km",
            'total_locations': "    "+str(self.total_locations)
        }


# Track for a client
class Track(models.Model):
    raw_data = models.FileField(upload_to='raw/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def display_track(self):
        ret = {
            'description': str(self.description),
            'timestamp': self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
            'file_url': self.raw_data.url,
            'id': self.id,
        }
        return ret
