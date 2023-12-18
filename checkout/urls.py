from django.urls import path

from checkout.views import CheckoutView, MpesaCallbackView, MpesaTransactionsView

urlpatterns = [
    path("pay/", CheckoutView.as_view(), name="pay"),
    path("callback/", MpesaCallbackView.as_view(), name="mpesa-callback"),
    path(
        "transactions/",
        MpesaTransactionsView.as_view(),
        name="mpesa-transactions",
    ),
]
