from django.conf.urls import include, url
from django.contrib.auth.views import logout
from django.conf import settings
from . import views

app_name = 'ecommerce'

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^checkout/$', views.checkout, name='checkout'),
	url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]