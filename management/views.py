from management.utils import *
# Create your views here.
class ViewSettingsPage(FormView):
    template_name = 'management/settings.html'
    form_class = SettingForm
    success_url = reverse_lazy('website:homepage')

    def get_initial(self):
        return get_initial_setting()

    def form_valid(self, form):
        data = form.cleaned_data
        update_setting(data)
        return super().form_valid(form)

class ViewUserManagementPage(TemplateView):
    template_name = 'management/user_management.html'

    def get_context_data(self, *args, **kwargs):
        context = {
            'Managers': Manager.objects.all()
        }

class UpdateLenseModelsView(TempalteView):
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

def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "management/upload_csv.html", data)
    # if not GET, then proceed
    read_csv(request)
    return HttpResponseRedirect(reverse("website:homepage"))
