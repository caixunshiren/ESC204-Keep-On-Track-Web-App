# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
import pandas as pd
import numpy as np
import haversine as hs
from haversine import Unit
from django.core.files.base import File
from zipfile import ZipFile


# Metadata
class MetaData(models.Model):
    total_clients = models.IntegerField(blank=True, default=0)
    total_time = models.FloatField(blank=True, default=0.0)
    total_distance = models.FloatField(blank=True, default=0.0)
    total_locations = models.FloatField(blank=True, default=0.0)
    total_time_saved = models.FloatField(blank=True, default=0.0)
    zip_file = models.FileField(upload_to='processed/', blank=True)

    def refresh(self):
        self.total_clients = Track.objects.count()
        total_time = 0
        total_distance = 0
        total_time_saved = 0
        for track in Track.objects.iterator():
            total_time += track.total_hours
            total_distance += track.total_distance
            total_time_saved += (track.average_speed/5) * track.total_hours
        self.total_time = total_time
        self.total_distance = total_distance
        self.total_time_saved = total_time_saved
        # to be completed
        # self.total_locations = Track.objects.count()
        self.save()

    def create_zip(self):
        with ZipFile('uploadfiles/temp.zip', 'w') as zipObj:
            # Add multiple files to the zip
            for track in Track.objects.iterator():
                zipObj.write(track.processed_csv.path)
        with open('uploadfiles/temp.zip', 'rb') as f:
            self.zip_file.save("all_tracks", File(f))
        self.save()
        print("aggregated_export")


    def display(self):
        return {
            'total_clients': "    "+str(self.total_clients),
            'total_time': "    "+str(round(self.total_time, 2))+" hours",
            'total_distance': "    "+str(round(self.total_distance, 2))+" km",
            'total_locations': "    "+str(round(self.total_locations, 2)),
            'total_time_saved': "    "+str(round(self.total_time_saved, 2)),
        }


# Track for a client
class Track(models.Model):
    raw_data = models.FileField(upload_to='raw/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_hours = models.FloatField(default=0, blank=True)
    total_distance = models.FloatField(default=0, blank=True)
    average_speed = models.FloatField(default=0, blank=True)
    total_time_saved = models.FloatField(default=0, blank=True)
    processed_csv = models.FileField(upload_to='processed/', blank=True)

    def display_track(self):
        ret = {
            'description': str(self.description),
            'timestamp': self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
            'file_url': self.raw_data.url,
            'id': str(self.id),
            'total_hours': str(round(self.total_hours, 3)),
            'total_distance': str(round(self.total_distance, 3)),
            'average_speed': str(round(self.average_speed, 2)),
            'total_time_saved': str(round(self.total_time_saved, 2)),
            'processed_url': self.processed_csv.url
        }
        return ret

    def load_file(self):  # returns pandas df object from file
        data = pd.read_csv(self.raw_data.file, delim_whitespace=True)
        data.columns = ['latitude', 'longitude', 'time']
        return data.astype(float)

    def compute_meta_data(self):
        try:
            data = self.load_file()
            total_time = 0
            total_distance = 0
            speed = []
            avg_speed = 0
            # check movement
            data['moving'] = True
            data['speed (km/h)'] = np.nan
            data['distance (m)'] = np.nan
            data['time delta (s)'] = np.nan
            for i in data.index:
                if i == 0:
                    continue
                cur_loc = (data.iloc[i]['latitude'], data.iloc[i]['longitude'])
                last_loc = (data.iloc[i-1]['latitude'], data.iloc[i-1]['longitude'])
                if last_loc[0] == cur_loc[0] and last_loc[1] == cur_loc[1]:
                    data.iloc[i]['moving'] = False

            for i in data.index:
                if i == 0 or not data.iloc[i]['moving']:
                    continue
                cur_loc = (data.iloc[i]['latitude'], data.iloc[i]['longitude'])
                last_loc = (data.iloc[i-1]['latitude'], data.iloc[i-1]['longitude'])
                delta_t = abs(data.iloc[i]['time'] - data.iloc[i-1]['time'])
                dis = hs.haversine(cur_loc, last_loc, unit=Unit.METERS)
                total_time += delta_t
                total_distance += dis
                speed.append((dis/delta_t)*3.6)  # convert to km/h
                data.at[i, 'distance (m)'] = dis
                data.at[i, 'speed (km/h)'] = (dis/delta_t)*3.6
                data.at[i, 'time delta (s)'] = delta_t
            avg_speed = sum(speed)/len(speed)
            self.total_distance = total_distance/1000  # convert to km
            self.total_hours = total_time/3600  # convert to hours
            self.average_speed = avg_speed
            self.total_time_saved += (self.average_speed / 5) * self.total_hours
            # print("success", total_distance, total_time/3600, avg_speed)
            # save data
            data.to_csv('uploadfiles/temp.csv', index=False)
            with open('uploadfiles/temp.csv') as f:
                self.processed_csv.save(f"{self.id}_processed", File(f))
            self.save()
        except:
            print("failed computing meta data for", self.description)
