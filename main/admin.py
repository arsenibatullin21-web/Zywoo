from django.contrib import admin

from main.models import Category, ProductImage, Product, Size, Color, PromoCode


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    list_display_links = ['name']
    fields = ['name', 'slug', 'description', 'image']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'quantity', 'discount' ,'description', 'available', 'created_at', 'updated_at']
    list_editable = ['price', 'quantity']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    actions = ['NotAv']
    inlines = [ProductImageInline]

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    fields = ['name', 'slug']
    search_fields = ['name']
    repopulated_fields = {'slug': ('name',)}

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    fields = ['name', 'slug', 'hex_code']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount']
    fields = ['name', 'discount']

