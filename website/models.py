from django.db import models

from django.contrib.auth.models import User

from management.models import Lense

class LenseInQueue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lense = models.ForeignKey(Lense, on_delete=models.CASCADE)

    def __str__(self):
        return "Lense Queue for " + str(self.user)

class SavedQueue(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_items_in_queue(self):
        return SavedQueueItem.objects.filter(queue=self)

class SavedQueueItem(models.Model):
    queue = models.ForeignKey(SavedQueue, on_delete=models.CASCADE)
    lense = models.ForeignKey(Lense, on_delete=models.CASCADE)

    def __str__(self):
        return "Lense Queue for " + str(self.user)
