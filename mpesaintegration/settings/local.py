from decouple import config
from mpesaintegration.settings.base import ALLOWED_HOSTS

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")]
)

DEBUG = True
