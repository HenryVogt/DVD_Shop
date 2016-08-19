# -*- coding: utf-8 -*-
from werkzeug.wrappers import Response, Request
import cPickle

from util.database import Database_wrapper as dbw
from templates.customer_list_view_renderer import render as render_customers
from templates.order_list_view_renderer import render as render_orders
from templates.product_list_view_renderer import render as render_products
from templates.frontend_list_view_renderer import render as render_frontend
from util.error import Error404
from util.context import get_default_context, get_default_context_frontend


import config


def list_view(request, context, db_info, render_func):
    ### Daten wiederherstellen

    # Defaults
    page = 1
    search_dict = {}
    pages_to_come = 0
    pages_count = 0
    list_data_dict = {}
    search_str = ""
    sort_by = None
    sort_order = 'ASC'
    session_sort = {}
    precise = False
    
    # GET-Path args
    if 'page' in request.path_args:
        page = request.path_args['page']

    # GET args request.args[key]
    for column in db_info['cols']:
        if column in request.args and len(request.args[column]):
            search_dict[column] = request.args[column]
    if 'precise' in request.args and request.args['precise'].upper() == 'TRUE':
        precise = True
            
    if 'search' in request.args and len(request.args['search']):
        search_str = request.args['search']

    # Session Data request.session[key]
    if 'sort' in request.session:
        session_sort = cPickle.loads(request.session['sort'])
        if context['section_path'] in session_sort and 'sort_by' in session_sort[context['section_path']] and 'sort_order' in session_sort[context['section_path']]:
            sort_by = session_sort[context['section_path']]['sort_by']
            sort_order = session_sort[context['section_path']]['sort_order']

     # POST Data  request.form[key]
    if 'sort_by' in request.form and request.form['sort_by'] in db_info['cols']:
        if sort_by:
            if sort_by == request.form['sort_by']:
                sort_order = 'ASC' if sort_order == 'DESC' else 'DESC'
            else:
                sort_order = 'ASC'
        sort_by = request.form['sort_by']

    if 'add_to_basket' in request.form:
        if 'basket' not in request.session:
            request.session['basket'] = {}
        if request.form['add_to_basket'] not in request.session['basket']:
            request.session['basket'][request.form['add_to_basket']] = 1
        else:
            request.session['basket'][request.form['add_to_basket']] += 1

    with dbw() as db:
        list_data_dict = db.get_objects(
            db_info, 
            block_offset = page - 1, 
            block_size = config.PAGE_SIZE, 
            search_str = search_str, 
            search_dict = search_dict,
            sort_by = sort_by,
            sort_order= sort_order,
	        precise = precise
        )
	
        # Wenn keine Datensätze und nicht auf der ersten Seite, kann es die Seite nicht geben
        if page > 1 and not len(list_data_dict):
            raise Error404("Seite nicht gefunden")

        items_count = db.get_count(db_info, search_str = search_str, search_dict = search_dict, precise = precise)
        # Wie viele Seiten gibt es?
        pages_count = items_count / config.PAGE_SIZE + (not not items_count % config.PAGE_SIZE)

        # Kommen noch Seiten?
        pages_to_come = pages_count - page

    # Daten manipulieren
    query_items = ["%s=%s" % (k,v) for k,v in search_dict.items()]
    query_items.extend(["search=%s" % search_str] if len(search_str) else [])
    query_items.extend(["precise=%s" % str(precise)] if precise else [])
    query_path = "?" + "&".join(query_items) if query_items else ""

    if pages_count == 0:
        pages_count = 1
    
    # Daten schreiben in context dict

    if search_dict or search_str:
        context['section_title'] = "%s – Suchergebnisse" % context['section_title']


    context.update({
        'page': page,
        'pages_to_come': pages_to_come,
        'pages_count': pages_count,
        'list_data_dict': list_data_dict,
        'query_path': query_path,
        'search_str' : search_str,
    })

    # Daten schreiben in session
    if not context['section_path'] in session_sort:
        session_sort[context['section_path']] = {}
    session_sort[context['section_path']]['sort_by'] = sort_by
    session_sort[context['section_path']]['sort_order'] = sort_order
    request.session['sort'] = cPickle.dumps(session_sort)
    # Letztendlich: An den Renderer schicken und in den Response laden
    return Response(render_func(context), content_type = "text/html" )

def customer_list_view(request):
    return list_view(request, get_default_context(request), config.DB_CUSTOMER, render_customers)

def order_list_view(request):
    return list_view(request, get_default_context(request), config.DB_ORDER, render_orders)

def product_list_view(request):
    return list_view(request, get_default_context(request), config.DB_PRODUCT, render_products)

def frontend_product_list_view(request):
    return list_view(request, get_default_context_frontend(request), config.DB_PRODUCT_AVAILABLE, render_frontend)
