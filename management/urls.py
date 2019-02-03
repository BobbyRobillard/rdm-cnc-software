from django.conf.urls import url, include

from management.views import (ViewSettingsPage, upload_csv, UpdateLenseModelsView,
								UpdateUserStatusView, DeleteUserView, AddUserView,
								ToggleCNCLockView)

# Application Routes (URLs)

app_name = 'management'

urlpatterns = [
    	# General Page Views
		# url(r'^$', views.homepage_view, name='homepage'),
		url(r'^settings/$', ViewSettingsPage.as_view(), name='settings'),
		url(r'^user-management/$', UpdateUserStatusView.as_view(), name='user_management'),
		url(r'^upload/csv/$', upload_csv, name='upload_csv'),
		url(r'^update-lense-models/$', UpdateLenseModelsView.as_view(), name='update_lense_models'),
		url(r'^delete-user/(?P<pk>\d+)/$', DeleteUserView.as_view(), name='delete_user'),
		url(r'^add-user/$', AddUserView.as_view(), name='add_user'),
		url(r'^toggle-cnc/(?P<pk>\d+)/(?P<toggle>\w+)/$', ToggleCNCLockView.as_view(), name='toggle_cnc'),
]
