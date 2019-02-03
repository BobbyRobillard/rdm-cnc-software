from management.utils import *
from management.mixins import ManagerRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ViewSettingsPage(LoginRequiredMixin, FormView):
    template_name = 'management/settings.html'
    form_class = SettingForm
    success_url = reverse_lazy('website:homepage')

    def get_initial(self):
        return get_initial_setting()

    def form_valid(self, form):
        data = form.cleaned_data
        update_setting(data)
        return super().form_valid(form)


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
            return super(DeleteMonitorView,self).render_to_response(context, **response_kwargs)


class ToggleCNCLockView(ManagerRequiredMixin, UpdateView):
    model = Setting
    form_class = SettingForm
    success_url = reverse_lazy('management:homepage')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.cnc_is_locked:
            self.object.cnc_is_locked = False
        else:
            self.object.cnc_is_locked = True
        self.object.save()
        context = self.get_context_data(object=self.object) # we dont need this but its safe to have
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax(): #checks if the request is ajax
            return JsonResponse({'toggled': True}, safe=False, **response_kwargs)
        else: # if not, returns a normal response
            return super(UpdateProposalView ,self).render_to_response(context, **response_kwargs)

def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "management/upload_csv.html", data)

    if read_csv(request):
        messages.success(request, "CSV Uploaded Successfully")
    else:
        messages.error(request, "Error uploading CSV")

    return redirect('management:upload_csv')
