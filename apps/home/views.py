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


# configs:
DEFAULT_CENTER = [2.770433, 32.442843]
KEY_LOCATIONS = {
    "Guru": [2.770433, 32.299843],
    "Pader": [2.881608, 33.085398],
    "Lira": [2.249377, 32.898580],
    "Atiak": [3.257736, 32.122098],
    "Anaka": [2.598748, 31.951074]
}


def map_control(m):
    for name in KEY_LOCATIONS.keys():
        folium.Marker(location=KEY_LOCATIONS[name], popup=name).add_to(m)
        folium.Circle(location=KEY_LOCATIONS[name], radius=10000, fill_color='gray', color='opaque').add_to(m)
    return m


def index(request):
    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        # print("debug post")
        if form.is_valid():
            form.save()
            # print("save")
            return redirect('home')
    else:
        form = TrackForm()
    # first time user
    from .models import MetaData
    if not MetaData.objects.exists():
        meta_data = MetaData()
        meta_data.refresh()
        meta_data.save()
    else:
        meta_data = [meta.display() for meta in MetaData.objects.iterator()][0]

    # folium
    m = folium.Map(location=DEFAULT_CENTER, zoom_start=9)
    m = map_control(m)
    folium.LayerControl().add_to(m)
    ## exporting
    m = m._repr_html_()

    return render(request, 'home/index.html', {
        'form': form,
        'map': m,
        'meta_data': meta_data
    })
    # return HttpResponse(html_template.render(context, request))


def data(request):
    from .models import Track
    tracks = [track.display_track() for track in
                              Track.objects.order_by('-uploaded_at').iterator()]
    return render(request, 'home/data.html', {'display_track': tracks})


def track_delete(request, id):
    from .models import Track
    track = Track.objects.get(id=id)
    track.delete()
    return redirect('data')


def refresh(request):
    from .models import MetaData
    if not MetaData.objects.exists():
        meta_data = MetaData()
        meta_data.refresh()
        meta_data.save()
    else:
        [meta.refresh() for meta in MetaData.objects.iterator()]
    return redirect('home')


def export(request):
    from .models import MetaData
    if not MetaData.objects.exists():
        meta_data = MetaData()
        meta_data.refresh()
        meta_data.save()
    else:
        [meta.refresh() for meta in MetaData.objects.iterator()]
    meta = [meta for meta in MetaData.objects.iterator()][0]
    meta.aggregated_export()
    return redirect('data')

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
