from django.db import models
from shop.mixins.models_mixins import SingletonModel


class Config(SingletonModel):
    contact_form_email = models.EmailField()
