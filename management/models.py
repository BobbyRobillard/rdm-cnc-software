from django.db import models

from django.contrib.auth.models import User

name_length = 100
decimal_digits = 2
max_digits = 6

class StandardBandit(models.Model):
    name = models.CharField(max_length=name_length)
    abbreviation = models.CharField(max_length=3, unique=True)
    initial_height = models.DecimalField(default=0, max_digits=max_digits, decimal_places=decimal_digits)

    def __str__(self):
        return str(self.abbreviation)

class Lense(models.Model):
    make = models.CharField(max_length=name_length)
    model = models.CharField(max_length=name_length)
    diameter = models.DecimalField(default=0, max_digits=max_digits, decimal_places=decimal_digits)
    height = models.DecimalField(default=0, max_digits=max_digits, decimal_places=decimal_digits)
    type = models.CharField(max_length=5)
    custom_band_size = models.ForeignKey(StandardBandit, blank=True, null=True, on_delete=models.SET_NULL)
    amount_processed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.make) + ' | ' + str(self.model) + ' | ' + str(self.type)

    def findSizePart2(self):
        sizePart2 = ""
        height = self.height
        if height <= 30:
            sizePart2 = "s"
        elif height >= 31 and height <= 42:
            sizePart2 = "m"
        else:
            sizePart2 = "l"
        return sizePart2

    def get_band_size(self):
        if self.custom_band_size:
            return self.custom_band_size

        sizePart1, sizePart2 = "", ""

        if self.diameter <= 75:
            if self.diameter >= 70 and self.height > 20:
                sizePart1 = "M"
                sizePart2 = self.findSizePart2()
            else:
                sizePart1 = "S"

        elif self.diameter >= 76 and self.diameter <= 93:
            sizePart1 = "M"
            sizePart2 = self.findSizePart2()

        else:
            sizePart1 = "L"

        return StandardBandit.objects.get(abbreviation=sizePart1 + sizePart2)


class Setting(models.Model):
    small_plunge_distance = models.DecimalField(default=0, max_digits=max_digits, decimal_places=decimal_digits)
    medium_plunge_distance = models.DecimalField(default=0, max_digits=max_digits, decimal_places=decimal_digits)
    large_plunge_distance = models.DecimalField(default=0, max_digits=max_digits, decimal_places=decimal_digits)
    cnc_is_locked = models.BooleanField(default=False)
    recent_orders_to_retain = models.PositiveIntegerField(default=0)
    cnc_task = models.ForeignKey('website.LenseInQueue', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "System Settings"
