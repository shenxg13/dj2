# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from blueapps.core.celery.celery import app


@app.task
def add(x, y):
    return x + y
