from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView

from main.models import Product, Category


# Create your views here.

class HomePageView(ListView):
    model = Product
    template_name = 'main/home.html'
    context_object_name = 'products_all'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['cover_products'] = Product.objects.exclude(category__slug__iexact='bags')
        context['products_bags'] = Product.objects.filter(category__slug='bags')
        return context


class CatalogFilterMixin:
    def apply_filters(self, queryset):
        category = self.request.GET.get('category', '')
        gender = self.request.GET.get('gender', '')
        size = self.request.GET.get('size', '')
        colors = self.request.GET.getlist('color')
        sort = self.request.GET.get('sort', '')

        if category:
            queryset = queryset.filter(category__slug=category)

        if gender and not getattr(self, 'gender', None):
            queryset = queryset.filter(gender=gender)

        if size:
            queryset = queryset.filter(variants__size__slug=size)

        if colors:
            queryset = queryset.filter(variants__color__slug__in=colors)

        if sort and sort != 'featured':
            if sort == 'highrate':
                queryset = queryset.order_by('-rating')
            elif sort == 'pricelow':
                queryset = queryset.order_by('price')
            elif sort == 'pricehigh':
                queryset = queryset.order_by('-price')
            elif sort == 'newtoold':
                queryset = queryset.order_by('-created_at')

        return queryset.distinct()




class CatalogPageView(CatalogFilterMixin, ListView):
    model = Product
    template_name = 'main/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        return self.apply_filters(queryset)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category', '')

        context['category'] = Category.objects.filter(slug=category).first()
        context['categories'] = Category.objects.all()
        context['selected_size'] = self.request.GET.get('size', '')
        context['selected_gender'] = self.request.GET.get('gender', '')
        context['selected_colors'] = self.request.GET.getlist('color')
        context['selected_sort'] = self.request.GET.get('sort', 'featured')
        context['total_products'] = Product.objects.all().count()
        context['catalog_clear_url'] = reverse('main:catalog')
        context['show_gender_filter'] = True
        return context

    def get_template_names(self):
        if self.request.headers.get('HX-Request') == 'true':
            return ['main/partials/catalog_partial.html']
        return ['main/catalog.html']




class GenderPageView(CatalogFilterMixin, ListView):
    model = Product
    gender = None
    template_name = 'main/gender_catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.filter(available=True, gender=self.gender)
        return self.apply_filters(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category', '')

        context['category'] = Category.objects.filter(slug=category).first()
        context['categories'] = Category.objects.all()
        context['selected_size'] = self.request.GET.get('size', '')
        context['selected_gender'] = self.request.GET.get('gender', '')
        context['selected_colors'] = self.request.GET.getlist('color')
        context['selected_sort'] = self.request.GET.get('sort', 'featured')

        context['catalog_gender'] = self.gender
        context['catalog_title'] = 'Men' if self.gender == 'men' else 'Women'
        context['total_products'] = Product.objects.filter(available=True, gender=self.gender).count()
        context['catalog_clear_url'] = reverse('main:men_catalog' if self.gender == 'men' else 'main:women_catalog')
        context['show_gender_filter'] = False
        return context

    def get_template_names(self):
        if self.request.headers.get('HX-Request') == 'true':
            return ['main/partials/catalog_partial.html']
        return ['main/gender_catalog.html']


