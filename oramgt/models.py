# -*- coding: utf-8 -*-

from django.db import models


class OraDbInfo(models.Model):
    hostname = models.CharField(max_length=100)
    ip_addr = models.CharField(max_length=100)
    port_num = models.IntegerField()
    srv_name = models.CharField(max_length=20)
    inst_name = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    awr_enabled = models.BooleanField(default=False)
    insp_enabled = models.BooleanField(default=False)
    logmon_enabled = models.BooleanField(default=False)
    tsmon_enabled = models.BooleanField(default=False)
    asmmon_enabled = models.BooleanField(default=False)
    production = models.BooleanField(default=True)

    class Meta:
        unique_together = ("ip_addr", "port_num", "inst_name")
