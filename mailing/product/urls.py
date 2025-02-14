from django.conf.urls import url, include
from . import views

app_name = 'product'

urlpatterns = [
    url(r'track_email_open/(?P<tracking_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/', views.track_email_open, name='track_email_open'),
    url(r'^create_order', views.create_order, name="create_order"),
    url(r'^', views.test, name="test"),
] 