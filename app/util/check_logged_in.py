# -*- coding: utf-8 -*-
from util.database import Database_wrapper as dbw

import config

def check_logged_in(request):
    username = ""
    customerid = ""
    # GET-Path args
    
    # GET args request.args[key]

    # POST Data  request.form[key]
    if 'username' and 'pw' in request.form:
        username = request.form['username']
        customerid = request.form['pw']

    # Session Data request.session[key]
 
    # ---- Daten aus dem Datenmodell holen
    
    # Daten manipulieren
    if not 'customerid' in request.session or not request.session['customerid']:
        if username and customerid:
            with dbw() as db:
                db_customerid = db.get_object(config.DB_LOGIN, customerid)['customerid']
                if str(db_customerid) == customerid:                    
                    request.session['customerid'] = customerid
                    return True
    else:
        return False