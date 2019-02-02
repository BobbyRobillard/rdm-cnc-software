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

def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "management/upload_csv.html", data)
    return read_csv(request)
