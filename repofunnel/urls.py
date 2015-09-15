"""repofunnel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import copr2pulp.views
import copr2pulp.restapi

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(copr2pulp.restapi.make_urls())),
    url(r'^repositories$', copr2pulp.views.repo_overview, name='repo_overview'),
    url(r'^$', copr2pulp.views.funnel_app, name='home'),
]
