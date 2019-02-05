from management.utils import *
from django.contrib.auth.mixins import UserPassesTestMixin



class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False
