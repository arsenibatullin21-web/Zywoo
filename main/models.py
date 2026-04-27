from decimal import Decimal

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=False, blank=False)
    image = models.ImageField(upload_to='category', blank=True)
    description = models.TextField(max_length=250)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['name'])
        ]

    def  __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('', kwargs={'slug': self.slug})


class Size(models.Model):
    name = models.DecimalField(max_digits=10, decimal_places=1, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Color(models.Model):
    name = models.DecimalField(max_digits=10, decimal_places=1, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    main_image = models.ImageField(upload_to='products/main/%Y/%m/%d')
    discount = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=10)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)
    size = models.ManyToManyField('Size',  related_name='products')
    color = models.ManyToManyField('Color', related_name='products')


    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.quantity > 0:
            self.available = True

    def final_price(self):
        if self.discount > 0:
            discount = self.price * Decimal(self.discount) / Decimal("100")
            return self.price - discount
        return self.price

    # def get_absolute_url(self):
    #     return reverse('', kwargs={''})




class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/gallery/%Y/%m/%d')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"{self.product.name} - {self.image.name}"


class PromoCode(models.Model):
    name = models.CharField(max_length=10, unique=True)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Promo Code'
        verbose_name_plural = 'Promo Codes'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

