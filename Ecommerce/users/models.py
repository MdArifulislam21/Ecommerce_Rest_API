
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from rest_framework.exceptions import NotAcceptable

from django.db.models.signals import post_save
from django.dispatch import receiver

# Initiallize user models to Django'es default User models
User = get_user_model()



class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image")
    bio = models.CharField(max_length=250, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Retrives Profiles query_set in reversely by created time
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()


class UserAddress(models.Model):
    # Address options
    BILLING = "B"
    SHIPPING = "S"

    ADDRESS_CHOICES = ((BILLING, _("billing")), (SHIPPING, _("shipping")))

    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    country = CountryField()
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    apartment = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()
    
    def __repr__(self):
        return self.user.get_full_name()
