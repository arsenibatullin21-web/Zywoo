from django.urls import path, include

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('catalog/', views.CatalogPageView.as_view(), name='catalog'),
    # path('catalog/<slug:category_slug>', views.CatalogPageView.as_view(), name='catalog_by_filter')
]