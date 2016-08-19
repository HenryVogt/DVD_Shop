# -*- coding: utf-8 -*-
import re

from werkzeug.wrappers import Response, Request

from util.error import Error404, Error503
from util.deliver_static import deliver_static
from util.split_path import split_path

from view.error404_view import error404_view
from view.error503_view import error503_view
from view.list_view import customer_list_view, order_list_view, product_list_view
from view.detail_view import customer_detail_view, order_detail_view, product_detail_view
from view.update_view import customer_update_view
from view.search_view import search_view_customer, search_view_product, search_view_order


def routing(request):
    '''Anhand des Pfades zu Views weiterleiten oder statische Inhalte ausliefern'''

    # regex, function_to_call, [Tupel convert-funktionen], [Tupel variablennamen]
    # jede Regex-Gruppe mit variablennamen not None wird durch die convert-Funktion gehauen und unter dem entsprechenden Namen im Request abgelegt
    routes = (
        # Kunden Listenansicht
        (r'^/$', 
            customer_list_view,
            (None,),
            (None,),
            {'path': ['kunden']}
        ),

        # Kunden Listenansicht
        (r'^/(kunden)(/seite)?/?$',
            customer_list_view,
            (split_path, None),
            ('path', None)
        ),
        # Mit Parameter seite
        (r'^/(kunden/seite)/([123456789]\d*)/?$',
            customer_list_view, 
            (split_path, int), 
            ('path', 'page'),
        ),

        (r'^/(bestellungen)(/seite)?/?$',
            order_list_view,
            (split_path,None),
            ('path',None)
        ),
        # Mit Parameter seite
        (r'^/(bestellungen/seite)/([123456789]\d*)/?$',
            order_list_view, 
            (split_path, int), 
            ('path', 'page'),
        ),

        (r'^/(produkte)(/seite)?/?$', 
            product_list_view,
            (split_path,None),
            ('path',None)
        ),
        # Mit Parameter seite
        (r'^/(produkte/seite)/([123456789]\d*)?/?$', 
            product_list_view, 
            (split_path, int), 
            ('path', 'page'),
        ),
        
        # Kunde Details
        (r'^/(kunden)/([123456789]\d*)/?$', 
            customer_detail_view, 
            (split_path, int), 
            ('path', 'id')
        ),
        # Kunden Update
        (r'^/(kunden/update)/([123456789]\d*)/?$',
            customer_update_view,
            (split_path,int),
            ('path','id')
        ),
        # Bestellung Details
        (r'^/(bestellungen)/([123456789]\d*)/?$', 
            order_detail_view, 
            (split_path, int), 
            ('path', 'id')
        ),
        # Produkt Details
        (r'^/(produkte)/([123456789]\d*)/?$', 
            product_detail_view, 
            (split_path, int), 
            ('path', 'id')
        ),

             
        (r'^/(kunden/suche)/?$', 
            search_view_customer,
            (split_path,),
            ('path',)
        ),

        (r'^/(produkte/suche)/?$', 
            search_view_product,
            (split_path,),
            ('path',)
        ),

        (r'^/(bestellungen/suche)/?$', 
            search_view_order,
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
    for route in routes:
        match = re.match(route[0], request.path)
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