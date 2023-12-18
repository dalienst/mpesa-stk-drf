import requests
from rest_framework import status
from rest_framework.response import Response


def get_access_token(access_token_url, consumer_key, consumer_secret):
    auth_response = requests.get(access_token_url, auth=(consumer_key, consumer_secret))
    auth_data = auth_response.json()
    access_token = auth_data.get("access_token")

    if not access_token:
        return Response(
            {"error": "Unable to obtain access token"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return access_token
