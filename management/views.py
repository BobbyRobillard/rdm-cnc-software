from management.utils import *
from management.mixins import ManagerRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin




class UpdateLenseModelsView(LoginRequiredMixin, TemplateView):
    template_name = 'website/homepage.html'

    def get(self, request, *args, **kwargs):
        models = Lense.objects.filter(make=kwargs['make'])
        data = {
            'models': models.values_list('make', flat=True).distinct(),
        }
        return self.render_to_response(data)


    def render_to_response(self, data, **response_kwargs):
        if self.request.is_ajax(): #checks if the request is ajax
            return JsonResponse(data, safe=False, **response_kwargs)
        else: # if not, returns a normal response
            return super(UpdateLenseModelsView,self).render_to_response(context, **response_kwargs)

@login_required
def cnc_toggle_lock_view(request): # Simple if better than complex...
    if request.user.is_superuser:
        setting = Setting.objects.get(pk=1)
        setting.cnc_is_locked = (not setting.cnc_is_locked)
        setting.save()
    return redirect('website:homepage')

@login_required
def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "management/upload_csv.html", data)

    if read_csv(request):
        messages.success(request, "CSV Uploaded Successfully")
    else:
        messages.error(request, "Error uploading CSV")

    return redirect('management:upload_csv')

def get_cnc_task_view(request):
    context = {
        "task" : get_cnc_gcode()
    }
    return render(request, 'management/cnc_task.html', context)

def stop_cnc_view(request):
    if Setting.objects.get(pk=1).cnc_task is None:
        messages.error(request, "Error, there is no task to stop!")
    else:
        messages.success(request, "Cutter reset!")
        setting = Setting.objects.get(pk=1)
        item = setting.cnc_task
        item.delete()
        setting.cnc_task = None
        setting.save()
    return redirect('website:homepage')

def cut_view(request, pk):
    if cnc_is_locked():
        messages.error(request, 'CNC Machine is locked.')
    elif cnc_is_busy():
        messages.error(request, 'Cutting already in progress.')
    else:
        setting = Setting.objects.get(pk=1)
        setting.cnc_task = LenseInQueue.objects.get(pk=pk)
        setting.save()
        messages.success(request, 'Cutting started!')
    return redirect('website:homepage')
