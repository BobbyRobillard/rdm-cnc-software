from management.utils import *
from django.contrib.auth.mixins import UserPassesTestMixin



class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if Manager.objects.filter(user=self.request.user):
            return True
        else:
            return False
