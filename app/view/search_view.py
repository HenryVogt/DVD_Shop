# -*- coding: utf-8 -*-
from werkzeug.wrappers import Response, Request

from templates.search_view_renderer import render_customer 
from templates.search_view_renderer import render_product 
from templates.search_view_renderer import render_order

from util.error import Error404
from util.context import get_default_context, get_default_context_frontend

import config

def search_view_customer(request):
    # Letztendlich: An den Renderer schicken und in den Response laden
    return Response(render_customer(get_default_context(request)), content_type = "text/html")

def search_view_order(request):
    # Letztendlich: An den Renderer schicken und in den Response laden
    return Response(render_order(get_default_context(request)), content_type = "text/html")

def search_view_product(request):
    # Letztendlich: An den Renderer schicken und in den Response laden
    return Response(render_product(get_default_context(request)), content_type = "text/html")

def search_view_frontend(request):
    # Letztendlich: An den Renderer schicken und in den Response laden
    return Response(render_product(get_default_context_frontend(request)), content_type = "text/html")

