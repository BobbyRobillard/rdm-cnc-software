from django.db import models

from django.contrib.auth.models import User

from management.models import Lense

class Queue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lenses = models.ManyToManyField(Lense)

    def __str__(self):
        return "Queue for %s" % self.user
