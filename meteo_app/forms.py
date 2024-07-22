from django import forms

from meteo_app.models import UserHistory


class MeteoForm(forms.ModelForm):

    class Meta:
        model = UserHistory
        fields = ['city']
