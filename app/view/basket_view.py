# -*- coding: utf-8 -*-
from werkzeug.wrappers import Response

from util.database import Database_wrapper as dbw

from util.context import get_default_context_frontend

from templates.frontend_basket_view_renderer import render as render_basket

import config
from datetime import datetime

BASKET_OK = "Ihre Bestellung wird in den nächsten Tagen geliefert"
BASKET_NOTOK = "In Ihrem Warenkorb war ein Artikel nicht mehr verfügbar"

def basket_view(request):
    ### Daten wiederherstellen
    newProduct = ""
    delete = False
    order = False
    flashinfo = ""
    list_data_dict = []
    # GET-Path args

    # POST Data  request.form[key]
    if 'action' in request.form:
        delete = True if request.form['action'] == 'delete' else False
        order = True if request.form['action'] == 'order' else False

    # Session Data request.session[key]
    if 'basket' in request.session:
        basket = request.session['basket']
    else:
        basket = {}
        
    # ---- Daten aus dem Datenmodell holen
    
    # Daten manipulieren


    if delete:
        basket = {}

    if order and basket:
        checkedBasket = order_products(basket, request.session['customerid'])
        flashinfo = BASKET_OK if not checkedBasket else BASKET_NOTOK

        basket = checkedBasket

    # Daten schreiben in context dict
    context = get_default_context_frontend(request)
    
    if basket:
        with dbw() as db:
            list_data_dict = db.get_objects_forBasket(basket, config.DB_PRODUCT)

    print_list_data_dict = []

    for row in list_data_dict:
        row.update({ 'amount': basket[str(row['prod_id'])], 'totalprice': basket[str(row['prod_id'])]*row['price'] })
        print_list_data_dict.append(row)


    else:
        list_data_dict = dict()

    context.update({
        'list_data_dict': print_list_data_dict,
        'page': 1,
        'pages_to_come': 0,
        'pages_count': 1,
        'flash_info': flashinfo,
        'query_path' : "",
        'section_title': "Warenkorb"
    })
    request.session['basket'] = basket

    # Letztendlich: An den Renderer schicken und in den Response laden
    return Response(render_basket(context), content_type = "text/html")

def order_products(basket, customerid):

    with dbw() as db:
        list_data_dict = db.select_for_update(config.DB_INVENTORY, basket.keys())

        # Ueberpruefung, ob alle Waren noch da sind
        checkedBasket = map(lambda x:x>=int(basket[str(data['prod_id'])]), [int(data['quan_in_stock']) for data in list_data_dict]) # data[7] = quan_in_stock
        permit = False if False in checkedBasket else True

        if permit:
            # Bestellung speichern
            netamount = float(reduce(lambda x,y: x+y, [data['prod_id'] for data in list_data_dict])) # data[4]
            tax = netamount * config.TAX
            #customerid = db.get_object(config.DB_LOGIN, customerid)[0]
            values = {  'orderdate': datetime.now(), 
                        'customerid': customerid, 
                        'netamount': netamount, 
                        'tax': tax, 
                        'totalamount': netamount+tax }

            # INSERT und RETURNING orderid
            orderid = db.insert(config.DB_ORDER_INSERT, values)

            # Bestellposten eintragen, Inventar aktualisieren
            orderlineid = 0
            for prod_id in basket.keys():
                orderlineid += 1
                # INSERT ORDERLINES
                insert_values = {   'orderlineid': orderlineid, 
                                    'orderid': orderid,
                                    'prod_id': int(prod_id),
                                    'quantity': int(basket[prod_id]),
                                    'orderdate': datetime.now() }
                db.insert(config.DB_ORDERLINE_INSERT, insert_values)

                # sales + 1, quan_in_stock - 1
                update_info = { 'quan_in_stock':'quan_in_stock - %s' % basket[prod_id], 'sales':'sales + %s' % str(basket[prod_id]) }

                db.update_data_inventory(config.DB_INVENTORY, update_info, id = int(prod_id))

            # Alle geklappt? COMMIT
            db.commit()

            # Warenkorb leeren
            basket = {}
        else:
            # Fehlende Ware wird aus dem Warenkorb gelöscht
            db.rollback()


    return basket
