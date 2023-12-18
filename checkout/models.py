from django.db import models

from checkout.abstracts import TimeStampedModel, UniversalIdModel


class MpesaBody(UniversalIdModel, TimeStampedModel):
    body = models.JSONField()

    class Meta:
        ordering = ["-created_at"]


class Checkout(UniversalIdModel, TimeStampedModel):
    amount = models.BigIntegerField()
    phone = models.BigIntegerField()
    receipt = models.CharField(max_length=100, default="receipts")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.receipt} - {self.phone} - {self.amount}"
