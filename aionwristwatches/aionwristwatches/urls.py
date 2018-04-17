"""aionwristwatches URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from ecommerce import views as ecommerce_views
from django.conf.urls import handler400, handler403,handler404,handler500
urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^', include('ecommerce.urls', namespace='ecommerce')),
	url(r'session_security/', include('session_security.urls')),
]
handler400 = ecommerce_views.error_400
handler403 = ecommerce_views.error_403
handler404 = ecommerce_views.error_404
handler500 = ecommerce_views.error_500
