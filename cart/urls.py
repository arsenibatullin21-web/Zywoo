from django.contrib import admin
from django.urls import path, include

from cart import views

app_name = 'cart'
urlpatterns = [
    path('detail/', views.detail, name='detail'),
    path('add/<int:product_id>', views.add, name='add'),
    path('remove/<str:cart_key>', views.remove, name='remove'),
    path('clear/', views.clear, name='clear'),
    path('updateqty/<str:cart_key>', views.update_quantity, name='update_quantity'),

]