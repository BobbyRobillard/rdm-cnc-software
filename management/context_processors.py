from management.utils import *

def cnc_is_locked(request):
    return {
        "cnc_is_locked": Setting.objects.get(pk=1).cnc_is_locked
    }
