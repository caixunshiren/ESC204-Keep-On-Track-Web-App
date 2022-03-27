from django import forms
from apps.home.models import Track

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ('description', 'raw_data', )