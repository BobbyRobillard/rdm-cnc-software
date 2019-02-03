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

class UpdateUserStatusView(ManagerRequiredMixin, View):
    template_name = 'management/user_management.html'
    RoleFormSet = formset_factory(RoleForm, max_num=len(User.objects.all()))
    success_url = reverse_lazy('management:user_management')

    def get(self, *args, **kwargs):
        RoleFormSet = self.RoleFormSet(initial=[
        {
            'user': user,
            'role': UserMethods.is_manager(user)
        } for user in User.objects.all()
        ])
        for form, user in zip(RoleFormSet, User.objects.all()):
            form.fields['user'].queryset = User.objects.filter(username=user.username)
        context = {
            'RoleFormSet': RoleFormSet
        }
        return render(self.request, self.template_name, context)

    def post(self,request,*args,**kwargs):
        RoleFormSet=self.RoleFormSet(self.request.POST)
        added = False
        if RoleFormSet.is_valid():
            added = True
            for role in RoleFormSet:
                data = role.cleaned_data
                if data['role'] == 'Manager':
                    Manager.objects.update_or_create(user=data['user'],
                    defaults={
                        'user': data['user'],
                        }
                        )
                else:
                    if Manager.objects.filter(user=data['user']).exists():
                        manager = Manager.objects.filter(user=data['user'])
                        manager.delete()
            messages.success(request, "Users updated Successfully")
            return HttpResponseRedirect(reverse_lazy('management:user_management'))
        else:
            context = {
                'Managers': Manager.objects.all(),
                'users': User.objects.all(),
                'formset': self.RoleFormSet(initial=[
                {
                    'user': user,
                    'role': 'Manager'
                } for user in User.objects.all()
                ])
            }
            messages.error(request, "Users could not be updated")
        return render(self.request,self.template_name,context)



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

class AddUserView(ManagerRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'management/add_user.html'
    success_url = reverse_lazy('management:user_management')

class DeleteUserView(ManagerRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('management:user_management')

    # ajax sends a get request, which then deletes the object
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        context = self.get_context_data(object=self.object) # we dont need this but its safe to have
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax(): #checks if the request is ajax
            return JsonResponse({'deleted': True}, safe=False, **response_kwargs)
        else: # if not, returns a normal response
            return super(DeleteMonitorView,self).render_to_response(context, **response_kwargs)

class ToggleCNCLockView(ManagerRequiredMixin, UpdateView):
    model = Setting
    form_class = SettingForm
    success_url = reverse_lazy('management:homepage')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.cnc_is_locked = kwargs['toggle']
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
