# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from base.common import common_paginator
from .models import OraDbInfo
# from haystack.query import SearchQuerySet
import cx_Oracle
import os
from blueapps.account.decorators import login_exempt


# @login_exempt
def db_list(request, *args, **kwargs):
    db_list_all = OraDbInfo.objects.all().order_by("id")
    # paged = common_paginator(request, db_list_all, 10)
    paged = {"paged_obj": db_list_all}
    return render(request, "oramgt/db_list.html", {"paged": paged, "paginator_url": "db_list"})


# @login_exempt
# def db_search(request, *args, **kwargs):
#     query = request.GET.get("q")
#     if query:
#         db_list_filtered = SearchQuerySet().models(OraDbInfo).filter(content__contains=query)
#         paged_obj = []
#         paged = {"paged_obj": paged_obj}
#         for db in db_list_filtered:
#             paged_obj.append(db.object)
#         return render(request, "oramgt/db_list.html", {"paged": paged})
#     else:
#         return redirect(reverse("db_list"))


# @login_exempt
def db_retire(request, *args, **kwargs):
    db_id = request.POST.get("db-id")
    db = OraDbInfo.objects.get(id=db_id)
    db.production = False
    db.save()
    return redirect(reverse("db_list"))


# @login_exempt
def db_edit(request, *args, **kwargs):
    if request.method == "POST":
        db_id = request.POST.get("db-id")
        hostname = request.POST.get("hostname")
        ip_addr = request.POST.get("ip-addr")
        port_num = request.POST.get("port-num")
        srv_name = request.POST.get("db-name")
        inst_name = request.POST.get("inst-name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        awr_enabled = request.POST.get("enable-awr")
        insp_enabled = request.POST.get("enable-insp")
        logmon_enabled = request.POST.get("enable-logmon")
        tsmon_enabled = request.POST.get("enable-tsmon")
        asmmon_enabled = request.POST.get("enable-asmmon")
        production = request.POST.get("prod")
        if db_id:
            ora_db_info = OraDbInfo.objects.get(id=db_id)
            ora_db_info.hostname = hostname
            ora_db_info.ip_addr = ip_addr
            ora_db_info.port_num = port_num
            ora_db_info.srv_name = srv_name
            ora_db_info.inst_name = inst_name
            ora_db_info.username = username
            ora_db_info.password = password
            ora_db_info.awr_enabled = awr_enabled
            ora_db_info.insp_enabled = insp_enabled
            ora_db_info.logmon_enabled = logmon_enabled
            ora_db_info.tsmon_enabled = tsmon_enabled
            ora_db_info.asmmon_enabled = asmmon_enabled
            ora_db_info.production = production
            ora_db_info.save()
        else:
            ora_db_info = OraDbInfo(hostname=hostname, ip_addr=ip_addr, port_num=port_num, srv_name=srv_name,
                                    inst_name=inst_name, username=username, password=password, awr_enabled=awr_enabled,
                                    insp_enabled=insp_enabled, logmon_enabled=logmon_enabled,
                                    tsmon_enabled=tsmon_enabled,asmmon_enabled=asmmon_enabled, production=production)
            ora_db_info.save()
        return redirect(reverse("db_list"))
    else:
        db_id = request.GET.get("id")
        if db_id:
            db = OraDbInfo.objects.get(id=db_id)
        else:
            db = None
        return render(request, "oramgt/db_edit.html", {"db": db})