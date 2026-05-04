from django import forms

from main.models import Product


class ProductAddForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price', 'discount','category', 'description', 'main_image', 'rating', 'gender', 'available', 'slug']