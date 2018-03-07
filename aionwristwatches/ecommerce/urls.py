from django.conf.urls import include, url
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'ecommerce'

urlpatterns = [
    
	url(r'^$', views.index, name='index'),

    url(r'^uacct/$', views.uacct, name='uacct'),
    url(r'^prodman/$', views.prodman, name='prodman'),
    url(r'^loginmanager/$',views.loginmanager, name='loginmanager'),
    url(r'^adminman/$',views.adminman, name='adminman'),
    url(r'^adminman/prodmng/$',views.prodmng, name='prodmng'),
    url(r'^adminman/prodmng/editp/$',views.editp, name='editp'),
    url(r'^adminman/prodmng/addp/$',views.addp, name='addp'),
    url(r'^acctman/$',views.acctman, name='acctman'),
	url(r'^shipping/$',views.shipping, name='shipping'),
    url(r'^product/(?P<product_id>[0-9]+)/$', views.product, name='product'),
    url(r'^checkout/(?P<product_id>[0-9]+)/$', views.checkout, name='checkout'),
	url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
