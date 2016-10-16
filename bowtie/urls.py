"""bowtie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from bowtie_processor import views as processor

admin.autodiscover()

urlpatterns = [
	url(r'^$', processor.index, name='main'),
	url(r'^process/$', processor.process, name='process'),
	url(r'^process_text/$', processor.process_text, name='process_text'),
	url(r'^details/(?P<place_id>[a-zA-Z0-9_-]+)$', processor.process_details, name='details'),
    url(r'^admin/', admin.site.urls)
]
