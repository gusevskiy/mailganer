from django.conf.urls import url, include
from . import views

app_name = 'createmailing'

urlpatterns = [
    url(r'track_email_subscribed/(?P<tracking_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/',
        views.track_email_subscribed,
        name='track_email_subscribed'),
    url(r'track_email_unsubscribed/(?P<tracking_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/',
        views.track_email_unsubscribed,
        name='track_email_unsubscribed'),
    url(r'^', views.create_order, name="create_order"),
]
