from django.conf.urls import include, url
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'ecommerce'

urlpatterns = [
	url(r'^shipping/$',views.shipping, name='shipping'),
	url(r'^$', views.index, name='index'),
	url(r'^(?P<product_id>[0-9]+)/cart/$', views.add_to_cart, name='addcart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^uacct/$', views.uacct, name='uacct'),
    url(r'^product/(?P<product_id>[0-9]+)/$', views.product, name='product'),
	url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
