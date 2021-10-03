from django.db import models

class Spendings(models.Model):
    amount = models.DecimalField(max_digits=24, decimal_places=2)
    currency = models.CharField(max_length=3)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
