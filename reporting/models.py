from django.db import models

from management.models import Lense

class RecentOrder(models.Model):
    lenses = models.ManyToManyField(Lense)

class Diagnostic(models.Model):
    lense = models.ForeignKey(Lense, on_delete=models.CASCADE)
    amount_zoom_processed = models.PositiveIntegerField(default=0)
    amount_focus_processed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.lense) + ' | ' + str(self.amount_processed)
