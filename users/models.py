from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Confirmation code for {self.user.username}, confiration code: {self.code}"