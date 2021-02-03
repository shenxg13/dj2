# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^ora_test/$', views.ora_test, name='ora_test'),
]
