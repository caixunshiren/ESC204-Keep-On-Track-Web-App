# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from apps.home.forms import TrackForm
import folium
import os


def index(request):
    # print("index")
    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        # print("debug post")
        if form.is_valid():
            form.save()
            # print("save")
            return redirect('home')
    else:
        form = TrackForm()


    # folium
    m = folium.Map(location=[2.770433, 32.299843], zoom_start=14)

    folium.LayerControl().add_to(m)
    ## exporting
    m = m._repr_html_()


    return render(request, 'home/index.html', {
        'form': form,
        'map': m
    })
    # return HttpResponse(html_template.render(context, request))


def data(request):
    from .models import Track
    tracks = [track.display_track() for track in
                              Track.objects.order_by('-uploaded_at').iterator()]
    return render(request, 'home/data.html', {'display_track': tracks})


# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:
#
#         load_template = request.path.split('/')[-1]
#
#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = load_template
#
#         html_template = loader.get_template('home/' + load_template)
#         return HttpResponse(html_template.render(context, request))
#
#     except template.TemplateDoesNotExist:
#
#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))
#
#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))
