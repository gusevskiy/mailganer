from django.conf.urls import url, include
from . import views

app_name = 'product'

urlpatterns = [
    url('', views.create_order, name="create_order"),
] 