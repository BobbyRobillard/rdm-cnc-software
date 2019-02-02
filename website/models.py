from django.db import models
from django.contrib.auth.models import User
from management.models import Manager

class UserMethods(User):
  def is_manager(self):
      if Manager.objects.filter(user=self):
          return 'Manager'
      else:
          return 'Employee'

  class Meta:
    proxy=True
