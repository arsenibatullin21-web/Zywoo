from django.shortcuts import render
from django.views.generic import ListView

from main.models import Product, Category, Size


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


class CatalogPageView(ListView):
    model = Product
    template_name = 'main/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = None
        queryset = Product.objects.filter(available=True)

        size_slug = self.request.GET.get('size', '')
        gender_slug = self.request.GET.get('gender', '')
        category_slug = self.request.GET.get('category', '')
        color_slugs = self.request.GET.getlist('color')
        sort_slug = self.request.GET.get('sort', '')

        category = Category.objects.filter(slug=category_slug).first()
        size = Size.objects.filter(slug=size_slug).first()

        if category:
            self.category = category
            queryset = Product.objects.filter(category=category)

        if size:
            queryset = queryset.filter(variants__size__slug=size_slug)

        if gender_slug:
            queryset = queryset.filter(gender=gender_slug)

        if color_slugs:
            queryset = queryset.filter(variants__color__slug__in=color_slugs)

        if sort_slug and sort_slug != 'featured':
            if sort_slug == 'highrate':
                queryset = queryset.order_by('-rating')
            elif sort_slug == 'pricelow':
                queryset = queryset.order_by('price')
            elif sort_slug == 'pricehigh':
                queryset = queryset.order_by('-price')
            elif sort_slug == 'newtoold':
                queryset = queryset.order_by('-created_at')

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        context['selected_size'] = self.request.GET.get('size', '')
        context['selected_gender'] = self.request.GET.get('gender', '')
        context['selected_colors'] = self.request.GET.getlist('color')
        context['selected_sort'] = self.request.GET.get('sort', 'featured')
        context['total_products'] = Product.objects.all().count()
        return context

    def get_template_names(self):
        if self.request.headers.get('HX-Request') == 'true':
            return ['main/partials/catalog_partial.html']
        return ['main/catalog.html']

