from django.conf.urls import url, include

from . import views
from management.views import (upload_csv, UpdateLenseModelsView)

# Application Routes (URLs)

app_name = 'management'

urlpatterns = [
    	# General Page Views
		url(r'^upload/csv/$', upload_csv, name='upload_csv'),
		url(r'^update-lense-models/$', UpdateLenseModelsView.as_view(), name='update_lense_models'),
		url(r'^toggle-cnc/$', views.cnc_toggle_lock_view, name='toggle_cnc'),
		url(r'^get-task/$', views.get_cnc_task_view, name='get_task'),
		url(r'^cut/(?P<pk>\d+)/$', views.cut_view, name='cut'),
		url(r'^stop-cnc/$', views.stop_cnc_view, name='stop_cnc'),
]
