# -*- coding: utf-8 -*-
import re

from werkzeug.wrappers import Response, Request

from util.error import Error404, Error503
from util.deliver_static import deliver_static
from util.split_path import split_path
from util.check_logged_in import check_logged_in

from view.error404_view import error404_view
from view.error503_view import error503_view

from view.list_view import frontend_product_list_view
from view.detail_view import frontend_product_detail_view
from view.basket_view import basket_view
from view.search_view import search_view_frontend

from view.frontend_login_view import frontend_login_view

def routing(request):
    '''Anhand des Pfades zu Views weiterleiten oder statische Inhalte ausliefern'''

    # regex, function_to_call, [Tupel convert-funktionen], [Tupel variablennamen]
    # jede Regex-Gruppe mit variablennamen not None wird durch die convert-Funktion gehauen und unter dem entsprechenden Namen im Request abgelegt
    routes = (
        # Ohne Parameter
        (r'^/$', 
            frontend_product_list_view,
            (None,),
            (None,),
            {'path': ['produkte']}
        ),
        (r'^/(login)$', 
            frontend_login_view,
            (split_path,),
            ('path',)
        ),

        (r'^/(logout)$', 
            frontend_login_view,
            (split_path,),
            ('path',)
        ),

        (r'^/(produkte)/?$', 
            frontend_product_list_view,
            (split_path,),
            ('path',)
        ),

        (r'^/(produkte/seite)?/?$', 
            frontend_product_list_view,
            (split_path,),
            ('path',)
        ),
        # Mit Parameter seite
        (r'^/(produkte/seite)/([123456789]\d*)/?$', 
            frontend_product_list_view, 
            (split_path, int), 
            ('path', 'page'),
        ),

        (r'^/(warenkorb)/?$', 
            basket_view,
            (split_path,),
            ('path',)
        ),

        (r'^/(produkte/suche)/?$', 
            search_view_frontend,
            (split_path,),
            ('path',)
        ),
        
        # Spezialfall statische Inhalte
        (r'^/static/(.*)', 
            deliver_static, 
            (str,), 
            ('filename',)
        ),
    )

    request.path_args = {} 
    
    if not check_logged_in(request):
        path = '/login'
    if "customerid" in request.session and request.session["customerid"]:
        path = request.path
    
    for route in routes:
        match = re.match(route[0], path)
        # Wenn GET-Path in routing Regeln:
        if match:
            i = 0

            request.path_args['route_match'] = route[0]
            for group in match.groups():
                # Wenn für die Gruppe eine Konvertierungsregel und ein Name gegeben sind, fülle request damit
                if len(route) > 3 and route[2][i] and route[3][i]:
                    request.path_args[route[3][i]] = route[2][i](group)
                i += 1
            if len(route) > 4 and route[4]:
                request.path_args.update(route[4])
            try:
                return route[1](request)
            # Von den Views geworfene Exceptions verarbeiten
            except Error404 as e:
                request.error404_msg = e.msg
                return error404_view(request)
            except Error503 as e:
                request.error503_msg = e.msg
                return error503_view(request)

    request.error404_msg = "Seite nicht gefunden"
    return error404_view(request)


@Request.application
def application(request):
    request.session = request.environ["werkzeug.session"]
    request.script_root_ext = request.base_url[:-len(request.path)]
    return routing(request)