from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from cart.forms import CartAddForm
from main.forms import ProductAddForm
from main.models import Product, Category, Color, Size, ProductImage, ProductVariant


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
    paginate_by = 4

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
        context['selected_category'] = self.request.GET.get('category', '')
        context['total_products'] = Product.objects.all().count()
        context['catalog_clear_url'] = reverse('main:catalog')
        context['show_gender_filter'] = True


        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = query_params.urlencode()

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
    paginate_by = 4

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


class ProductDetailPageView(DetailView):
    model = Product
    template_name = 'main/product_detail.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_slug = self.kwargs.get('product_slug')
        product = Product.objects.filter(slug=product_slug).first()

        context['images'] = product.images.all()
        context['form'] = CartAddForm()
        context['colors'] = Color.objects.all()
        context['sizes'] = Size.objects.all()
        context["available_size_ids"] = product.variants.filter(
            available=True,
            quantity__gt=0
        ).values_list("size_id", flat=True)
        return context



class AddProductView(CreateView):
    model = Product
    template_name = 'main/create_product.html'
    form_class = ProductAddForm
    success_url = reverse_lazy('main:catalog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['variant_range'] = range(1, 4)
        context['sizes'] = Size.objects.all()
        context['colors'] = Color.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save()

        for image in self.request.FILES.getlist('gallery_images'):
            ProductImage.objects.create(
                product=self.object,
                image=image
            )

        for i in range(1, 4):
            size_id = self.request.POST.get(f'size_{i}', '')
            color_id = self.request.POST.get(f'color_{i}', '')
            sku = self.request.POST.get(f'sku_{i}', '')
            price = int(self.request.POST.get(f'price_{i}') or 0)
            discount = int(self.request.POST.get(f'discount_{i}') or 0)
            quantity = int(self.request.POST.get(f'quantity_{i}') or 0)
            image = self.request.FILES.get(f"image_{i}", '')

            if not size_id or not color_id or not sku or not price:
                continue

            ProductVariant.objects.create(
                product=self.object,
                size=Size.objects.get(id=size_id),
                color=Color.objects.get(id=color_id),
                sku=sku,
                price=price,
                discount=discount,
                quantity=quantity,
                image=image
            )

        return HttpResponseRedirect(self.get_success_url())