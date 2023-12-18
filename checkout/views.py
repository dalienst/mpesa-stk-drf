import requests
import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.utils import timezone

from checkout.serializers import CheckoutSerializer, MpesaBodySerializer
from checkout.models import Checkout, MpesaBody
from mpesaintegration.settings import (
    CONSUMER_SECRET,
    SHORTCODE,
    PASS_KEY,
    TRANSACTION_TYPE,
    CONSUMER_KEY,
    CALLBACK_URL,
)

from checkout.utils import get_access_token


class CheckoutView(generics.ListCreateAPIView):
    serializer_class = CheckoutSerializer
    queryset = Checkout.objects.all()

    def get_queryset(self):
        return Checkout.objects.all()

    def post(self, request, *args, **kwargs):
        # Extract values from request.data
        amount = request.data.get("amount")
        phone = request.data.get("phone")

        access_token = get_access_token(
            access_token_url="https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
        )

        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        shortcode = str(SHORTCODE)

        passkey = str(PASS_KEY)
        timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
        concatenated = f"{shortcode}{passkey}{timestamp}".encode()
        password = base64.b64encode(concatenated).decode()

        payload = {
            "BusinessShortCode": SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": TRANSACTION_TYPE,
            "Amount": amount,
            "PartyA": phone,
            "PartyB": SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": CALLBACK_URL,
            "AccountReference": "Test",
            "TransactionDesc": "Test",
        }

        # Make the API call
        api_response = requests.post(api_url, json=payload, headers=headers)
        response_data = api_response.json()
        return Response(response_data, status=api_response.status_code)


class MpesaCallbackView(APIView):
    def post(self, request, *args, **kwargs):
        callback_data = request.data

        if callback_data:
            MpesaBody.objects.create(body=callback_data)

            # Extract data from callback_data to create a Checkout instance
            amount = callback_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][
                0
            ]["Value"]
            phone_number = callback_data["Body"]["stkCallback"]["CallbackMetadata"][
                "Item"
            ][3]["Value"]
            receipt = callback_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][
                1
            ]["Value"]

            Checkout.objects.create(
                amount=amount,
                phone=phone_number,
                receipt=receipt,
            )

            return Response({"message": "Callback Data received successfully"})
        return Response(
            {"Failed": "No Callback Data Received"}, status=status.HTTP_400_BAD_REQUEST
        )


class MpesaTransactionsView(APIView):
    def get(self, request, *args, **kwargs):
        transactions = MpesaBody.objects.all()
        serializer = MpesaBodySerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
