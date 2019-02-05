from .models import Queue

from management.models import Lense

def add_to_queue(user, data):
    try:
        Queue.objects.get(user=user)
        q.add(Lense.objects.get(make=data['make'], model=data['model'], type=data['type']))
        q.save()
    except:
        q = Queue()
        q.save()
        q.user = user
        q.add(Lense.objects.get(make=data['make'], model=data['model'], type=data['type']))
        q.save()
