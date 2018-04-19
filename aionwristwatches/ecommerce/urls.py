from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import logout

from . import views

app_name = 'ecommerce'

urlpatterns = [
    
	url(r'^$', views.index, name='index'),
    url(r'^myorders/$', views.myorders, name='myorders'),
    url(r'^uacct/$', views.uacct, name='uacct'),
    url(r'^prodman/$', views.prodman, name='prodman'),
    url(r'^prodman/delete/$', views.proddelete, name='proddelete'),
    url(r'^prodman/add/$', views.prodadd, name='prodadd'),
    url(r'^prodman/edit/$', views.prodedit, name='prodedit'),
    url(r'^loginmanager/$',views.loginmanager, name='loginmanager'),
    url(r'^adminman/$',views.adminman, name='adminman'),
    url(r'^adminman/prodmng/$',views.prodmng, name='prodmng'),
    url(r'^adminman/acctmng/$',views.acctmng, name='acctmng'),
    url(r'^changepass/$', views.changepass, name='changepass'),
    url(r'^resetpass/$', views.resetpass, name='resetpass'),
    url(r'^adminman/prodmng/addp/$', views.addp, name='addp'),
    url(r'^adminman/acctmng/adda/$', views.adda, name='adda'),
    url(r'^acctman/$', views.acctman, name='acctman'),
    url(r'^product/(?P<product_id>[0-9]+)/$', views.product, name='product'),
    url(r'^checkout/(?P<product_id>[0-9]+)/$', views.checkout, name='checkout'),
	url(r'^logout/$', views.outlog, name='logout'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
