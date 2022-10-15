from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.CharField(max_length=10, default="£")
    
    def __str__(self):
        return self.currency