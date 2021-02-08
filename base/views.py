# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from .common import common_paginator
import cx_Oracle
from blueapps.account.decorators import login_exempt


@login_exempt
def index(request, *args, **kwargs):
    return redirect(reverse("db_list"))
