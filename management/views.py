from management.utils import *

# Create your views here.
class ViewSettingsPage(UpdateView):
    template_name = 'management/settings.html'
    model = Setting
    form_class = SettingForm
    success_url = reverse_lazy('website:homepage')
