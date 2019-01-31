from django.db import models

from management.models import Lense

class RecentOrder(models.Model):
    lenses = models.ManyToManyField(Lense)

class Diagnostic(models.Model):
    lense = models.ForeignKey(Lense, on_delete=models.CASCADE)
    amount_processed = models.PositiveIntegerField(default=0)
