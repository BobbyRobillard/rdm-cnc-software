from .models import LenseInQueue

from management.models import Lense

def add_to_queue(user, data):
    try:
        lense = Lense.objects.get(make=data['make'], model=data['model'],
                                  type=data['type'].lower())
    except:
        pass

    if data['custom_size']: # Check if user requests a different than generic band
        print("Setting custom size")
        lense.custom_band_size = data['custom_size']
        lense.save()

    LenseInQueue.objects.create(user=user, lense=lense)
