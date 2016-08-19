# -*- coding: utf-8 -*-
from werkzeug.wrappers import Response, Request

from templates.frontend_login_view_renderer import render as renderer_func
from util.error import Error404
from util.context import get_default_context
import config

def frontend_login_view(request):
    ### Daten wiederherstellen              
    # Daten schreiben in context dict
    if 'customerid' in request.session and request.session['customerid']:
        del request.session['customerid']

    context = get_default_context(request)    
    # Letztendlich: An den Renderer schicken und in den Response laden
    return Response(renderer_func(context), content_type = "text/html")

