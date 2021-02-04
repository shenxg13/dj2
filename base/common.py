# -*- coding: utf-8 -*-

from django.core.paginator import Paginator


def common_paginator(request, paging_obj, rows_per_page):
    paginator = Paginator(paging_obj, rows_per_page)
    current_page = int(request.GET.get("p") or 1)
    paged_obj = paginator.page(current_page)
    record_count = paginator.count
    last_page = paginator.num_pages
    if paged_obj.has_previous():
        previous_page = paged_obj.previous_page_number()
    else:
        previous_page = 1
    if paged_obj.has_next():
        next_page = paged_obj.next_page_number()
    else:
        next_page = current_page
    return {"paged_obj": paged_obj, "record_count": record_count, "current_page": current_page,
            "previous_page": previous_page, "next_page": next_page, "last_page": last_page}
