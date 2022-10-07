from django.db import models
from django.contrib.auth import get_user_model

from shop.mixins.models_mixins import PKMixin


class Feedback(PKMixin):
    text = models.TextField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
