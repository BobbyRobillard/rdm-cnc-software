from django.conf.urls import url, include

from . import views

# Application Routes (URLs)

app_name = 'website'

urlpatterns = [
    	# General Page Views
		url(r'^$', views.homepage_view, name='homepage'),
		url(r'^add-to-queue$', views.add_to_queue_view, name='add_to_queue'),
		url(r'^copy-item/(?P<pk>\d+)/$', views.copy_item_view, name='copy_item'),
		url(r'^delete-from-queue/(?P<pk>\d+)/$', views.delete_from_queue_view, name='delete_from_queue'),
		url(r'^change-model$', views.change_model_view, name='change_model'),
		url(r'^save-queue$', views.save_queue_view, name='save_queue'),
		url(r'^add-bands-from-queue/(?P<pk>\d+)/$', views.add_bands_from_queue_view, name='add_bands_from_queue'),
		url(r'^delete-saved-queue/(?P<pk>\d+)/$', views.delete_saved_queue_view, name='delete_saved_queue'),
]
