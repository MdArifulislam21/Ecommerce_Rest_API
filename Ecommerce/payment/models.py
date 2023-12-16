from django.db import models
from django.utils.translation import gettext_lazy as _
from Products.models import TimestampedModel
from orders.models import Order


class Payment(TimestampedModel):
    PENDING = "P"
    COMPLETED = "C"
    FAILED = "F"

    STATUS_CHOICES = (
        (PENDING, _("pending")),
        (COMPLETED, _("completed")),
        (FAILED, _("failed")),
    )
    
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    
    # Payment options
    BKASH = "B"
    PAYPAL = "P"
    
    PAYMENT_CHOICES = ((PAYPAL, _("paypal")), (BKASH, _("bkash")))

    
    payment_option = models.CharField(max_length=1, choices=PAYMENT_CHOICES)
    order = models.OneToOneField(
        Order, related_name="payment", on_delete=models.CASCADE
    )


    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.order.buyer.get_full_name()