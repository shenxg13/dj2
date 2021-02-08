# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
# from haystack.views import SearchView


urlpatterns = [
    url(r"^db_list/", views.db_list, name="db_list"),
    url(r"^db_retire/", views.db_retire, name="db_retire"),
    url(r"^db_edit/", views.db_edit, name="db_edit"),
    # url(r"^test_connection/", views.test_connection, name="test_connection"),
    # url(r"^db_search/", views.db_search, name="db_search"),
    # url(r"^oraawr/", include("oraawr.urls")),
    # url(r"^awr_db_list/$", views.awr_db_list, name="awr_db_list"),
    # url(r"^awr_rpt_list/$", views.awr_rpt_list, name="awr_rpt_list"),
    # url(r"^awr_rpt_detail/$", views.awr_rpt_detail, name="awr_rpt_detail"),
    # url(r"^awr_db_search/$", views.awr_db_search, name="awr_db_search"),
    # url(r"^awr_rpt_search/$", views.awr_rpt_search, name="awr_rpt_search"),
]