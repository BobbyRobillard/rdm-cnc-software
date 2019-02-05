from django.db import models

from django.contrib.auth.models import User

name_length = 100
decimal_digits = 2
max_digits = 6

class StandardBandit(models.Model):
    name = models.CharField(max_length=name_length)
    abbreviation = models.CharField(max_length=3)

    def __str__(self):
        return str(self.name)

class Lense(models.Model):
    height = models.DecimalField(default=0, max_digits=max_digits, decimal_places=decimal_digits)
    diameter = models.DecimalField(default=0, max_digits=max_digits, decimal_places=decimal_digits)
    make = models.CharField(max_length=name_length)
    model = models.CharField(max_length=name_length)
    custom_band_size = models.ForeignKey(StandardBandit, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.make) + ' | ' + str(self.model)

class Setting(models.Model):
    small_plunge_distance = models.DecimalField(default=0, max_digits=max_digits, decimal_places=decimal_digits)
    medium_plunge_distance = models.DecimalField(default=0, max_digits=max_digits, decimal_places=decimal_digits)
    large_plunge_distance = models.DecimalField(default=0, max_digits=max_digits, decimal_places=decimal_digits)
    cnc_is_locked = models.BooleanField(default=False)
    recent_orders_to_retain = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "System Settings"
