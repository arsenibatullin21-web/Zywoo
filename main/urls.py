from django.urls import path, include

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('collection/', views.CatalogPageView.as_view(), name='catalog'),
    path('catalog/mens/', views.GenderPageView.as_view(gender='men'), name='men_catalog'),
    path('catalog/women/', views.GenderPageView.as_view(gender='women'), name='women_catalog'),
    path('detial/<slug:product_slug>', views.ProductDetailPageView.as_view(), name='detail')
]
