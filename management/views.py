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
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("management:upload_csv"))
    #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("management:upload_csv"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
    #loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            fields = line.split(",")
            data = {}
            data['zoom_height'] = fields[0]
            print('field 0 good')
            data['zoom_diameter'] = fields[1]
            print('field 1 good')
            data['focus_height'] = fields[2]
            print('field 2 good')
            data['focus_diameter'] = fields[3]
            print('field 3 good')
            data['make'] = fields[4]
            print('field 4 good')
            data['model'] = fields[5]
            print('field 5 good')
            try:
                form = LenseForm(data)
                if form.is_valid():
                    form.save()
                    print('valid')
                else:
                    print(str(form.errors))
            except Exception as e:
                print(e)
                pass

    except Exception as e:
        print(e)

    return HttpResponseRedirect(reverse("website:homepage"))
