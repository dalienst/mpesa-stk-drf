from rest_framework import serializers
from checkout.models import Checkout, MpesaBody


class CheckoutSerializer(serializers.ModelSerializer):
    """
    Serializer to process the stk push
    """

    id = serializers.CharField(read_only=True)
    amount = serializers.IntegerField()
    phone = serializers.IntegerField()
    receipt = serializers.CharField(read_only=True)

    class Meta:
        model = Checkout
        fields = (
            "id",
            "amount",
            "phone",
            "receipt",
        )


class MpesaBodySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    body = serializers.JSONField(read_only=True)

    class Meta:
        model = MpesaBody
        fields = (
            "id",
            "body",
            "created_at",
        )
