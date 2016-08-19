# -*- coding: utf-8 -*-
import os
from datetime import datetime

# Database

DB_HOSTNAME = ""
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""


APP_NAME = "DVD Shop"
APP_NAME_ORDER = "DVD Shop"

NAVIGATION = [
    {'name': 'Kundendaten', 'path': 'kunden' },
    {'name': 'Bestellungen', 'path': 'bestellungen'},
    {'name': 'Produkte', 'path': 'produkte'},
   
]
NAVIGATION_ORDER = [
    {'name': 'Produkte', 'path': 'produkte' },
    {'name': 'Warenkorb', 'path': 'warenkorb' },
    {'name': 'Logout', 'path': 'logout' },
]


PAGE_SIZE = 15
TAX = 0.19

DB_ORDERLINES = {
    'cols': {
        'orderlineid': int, 
        'orderid': int,
        'quantity': int, 
        'prod_id': int, 
        'title': str
    },
    'table': 'orderlines_view',
    'key': 'orderlineid'
}

DB_ORDER = {
    'cols': {
        'orderid': int, 
        'orderdate': datetime.date, 
        'customerid': int, 
        'customer_firstname': str, 
        'customer_lastname': str, 
        'netamount': float, 
        'tax': float, 
        'totalamount': float
    },
    'table': 'orders_view',
    'key': 'orderid',
    'linked_table': DB_ORDERLINES,
}

DB_CUSTOMER = {
    'cols': {
        'customerid': int, 
        'firstname': str, 
        'lastname': str, 
        'address1': str, 
        'address2': str, 
        'city': str, 
        'state': str,
        'zip': int, 
        'country': str, 
        'region': int, 
        'email': str, 
        'phone': str, 
        'creditcardtype': int, 
        'creditcard': str, 
        'creditcardexpiration': str, 
        'username': str, 
        'password': str, 
        'age': int, 
        'income': int, 
        'gender': str
    },
    'table': 'customers',
    'key': 'customerid',
    'linked_table': DB_ORDER
}

DB_PRODUCT = {
    'cols': {
        'prod_id': int, 
        'categoryname': str, 
        'title': str, 
        'actor': str, 
        'price':float, 
        'special': int, 
        'common_prod_id': int, 
        'quan_in_stock': int
    },
    'table': 'products_view',
    'key': 'prod_id'
}

DB_PRODUCT_AVAILABLE = {
    'cols': {
        'prod_id': int, 
        'categoryname': str, 
        'title': str, 
        'actor': str, 
        'price':float, 
        'special': int, 
        'common_prod_id': int, 
        'quan_in_stock': int
    },
    'table': 'products_available_view',
    'key': 'prod_id'
}

DB_LOGIN = {
    'cols' : {'customerid' :int,},
    'table': 'customers',
    'key': 'customerid'
}

"""
DB_BASKET_PRODUCT = {
    'cols': {
        'prod_id': int, 
        'category': str, 
        'title': str, 
        'actor': str, 
        'price': float, 
        'quan_in_stock':int
    },
    'table': 'products_view',
    'key': 'prod_id'
}
"""
DB_INVENTORY = {
    'cols' : {'prod_id'
              'quan_in_stock',
              'sales'},

    'table' : 'inventory',
    'key'   : 'prod_id'
}

DB_ORDER_INSERT = {
    'cols' : {'orderdate': datetime.date,
              'customerid':int,
              'netamount': float,
              'tax': float,
              'totalamount': float},
    'table' : 'orders',
    'key' : 'orderid'
}

DB_ORDERLINE_INSERT = {
    'cols': {
        'orderlineid': int, 
        'orderid': int,
        'prod_id': int,
        'quantity': int, 
        'orderdate': datetime.date
    },
    'table': 'orderlines'
}


STATIC_FILE_DIR = 'static'
MIMETYPES = {
    'css' : 'text/css',
    'ttf' :  'application/font-sfnt',
    'otf' :  'application/font-sfnt',
    'woff':  'application/font-woff',
    'png' :  'image/png',
}

TEMPLATE_DIR = os.path.join('templates', 'markup')
TEMPLATE_FILE_EXT = '.tpl'
