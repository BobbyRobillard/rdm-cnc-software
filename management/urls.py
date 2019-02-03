from django.conf.urls import url, include

from management.views import (ViewSettingsPage, upload_csv, UpdateLenseModelsView,
								ToggleCNCLockView)

# Application Routes (URLs)

app_name = 'management'

urlpatterns = [
    	# General Page Views
		# url(r'^$', views.homepage_view, name='homepage'),
		url(r'^settings/$', ViewSettingsPage.as_view(), name='settings'),
		url(r'^upload/csv/$', upload_csv, name='upload_csv'),
		url(r'^update-lense-models/$', UpdateLenseModelsView.as_view(), name='update_lense_models'),
		url(r'^toggle-cnc/(?P<pk>\d+)/$', ToggleCNCLockView.as_view(), name='toggle_cnc'),
]
