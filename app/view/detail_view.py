# -*- coding: utf-8 -*-
from werkzeug.wrappers import Response, Request

from util.database import Database_wrapper as dbw

from templates.customer_detail_view_renderer import render as render_customer
from templates.customer_update_view_renderer import render as render_customer_update
from templates.order_detail_view_renderer import render as render_order
from templates.product_detail_view_renderer import render as render_product

from util.error import Error404
from util.context import get_default_context

import config

def detail_view(request, context, db_info, render_func):
    ### Daten wiederherstellen

    # Defaults
    id = 0
    detail_data_dict = {}
    detail_list_dict = {}

    # GET-Path args
    if 'id' in request.path_args:
        id = int(request.path_args['id'])

    # GET args request.args[key]

    # POST Data  request.form[key]

    # Session Data request.session[key]
 
    # ---- Daten aus dem Datenmodell holen
    with dbw() as db:
        detail_data_dict = db.get_object(db_info, key = id)
        if 'linked_table' in db_info:
            detail_list_dict = db.get_objects(db_info['linked_table'], search_dict = {db_info['key']: id})

    # Daten manipulieren


    # Daten schreiben in context dict
    context.update({
        'detail_data_dict': detail_data_dict,
        'detail_list_dict': detail_list_dict
    })
        
    # Letztendlich: An den Renderer schicken und in den Response laden
    return Response(render_func(context), content_type = "text/html")

def customer_detail_view(request):
    return detail_view(request, get_default_context(request), config.DB_CUSTOMER, render_customer)

def order_detail_view(request):
    return detail_view(request, get_default_context(request), config.DB_ORDER, render_order)

def product_detail_view(request):
    return detail_view(request, get_default_context(request), config.DB_PRODUCT, render_product)

def frontend_product_detail_view(request):
    return detail_view(request, get_default_context(request), config.DB_PRODUCT, render_product)
