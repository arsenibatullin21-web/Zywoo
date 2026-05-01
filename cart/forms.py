from django import forms

from main.models import Size, Color


class CartAddForm(forms.Form):
    size = forms.ModelChoiceField(queryset=Size.objects.all(), required=True)
    color = forms.ModelChoiceField(queryset=Color.objects.all(), required=True)

