from django.contrib import admin

from main.models import Category, ProductImage, Product, Size, Color, PromoCode, ProductVariant


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    list_display_links = ['name']
    fields = ['name', 'slug', 'parent','description', 'image']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'discount' , 'available', 'gender']
    list_editable = ['price']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'slug']
    fields = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'slug']
    fields = ['name', 'slug', 'hex_code']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount']
    fields = ['name', 'discount']


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'discount' ,'quantity', 'available', 'created_at', 'updated_at']
    list_editable = ['quantity']
    search_fields = ['product__name']
