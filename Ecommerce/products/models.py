from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()

"""
Abstract models class class. This models will inherit to 
other classes where need datetime fields.
"""
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def category_image_path(instance, filename):
    return f"category/icons/{instance.name}/{filename}"


def product_image_path(instance, filename):
    return f"product/images/{instance.name}/{filename}"


class Category(TimestampedModel):
    name = models.CharField(_("Category name"), max_length=100)
    icon = models.ImageField(upload_to=category_image_path, blank=True)
    
    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")
        
    def __str__(self):
        return self.name


def get_default_product_category():
    return Category.objects.get_or_create(name="Others")[0]


class Product(TimestampedModel):
    name = models.CharField(max_length=200)
    details = models.TextField()
    image = models.ImageField(upload_to=product_image_path)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)
    
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.SET(get_default_product_category),
    )
    seller = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name
