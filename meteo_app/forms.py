from django import forms


class MeteoForm(forms.Form):
    city = forms.CharField(label='Город', max_length=100)
