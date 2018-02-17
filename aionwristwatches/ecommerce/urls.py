from django.conf.urls import include, url
from . import views

app_name = 'ecommerce'

urlpatterns = [
	url(r'^$', views.index, name='index'),
]