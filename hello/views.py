# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .tasks import add
from blueapps.account.decorators import login_exempt
import cx_Oracle


@login_exempt
def ora_test(request, *args, **kwargs):
    try:
        ip_addr = request.GET.get('ip_addr')
        port_num = request.GET.get('port_num')
        srv_name = request.GET.get('srv_name')
        conn_str = f'{ip_addr}:{port_num}/{srv_name}'
        with cx_Oracle.connect('oraview', 'oracle', conn_str) as conn:
            with conn.cursor() as cur:
                sql_instance = 'select instance_number from v$instance'
                inst_num = cur.execute(sql_instance).fetchone()[0]
                return HttpResponse(inst_num)
    except Exception as e:
        raise e


@login_exempt
def hello(request, *args, **kwargs):
    res = add.delay(2, 3)
    return HttpResponse(res.get())
