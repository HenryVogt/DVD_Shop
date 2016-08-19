# -*- coding: utf-8 -*-
from werkzeug.wrappers import Response, Request

from util.database import Database_wrapper as dbw
from templates.customer_update_view_renderer import render as render_customer_update


from util.error import Error404
from util.context import get_default_context

import config

def update_view(request, context, db_info, render_func):

    id = 0
    row_data_dict = {}


    # GET-Path args
    if 'id' in request.path_args:
        id = int(request.path_args['id'])

    # Schlüssel zum Speichern der Daten in der Session
    key = '%s.%s.data' % (db_info['table'],id)

    with dbw() as db:
        # Prüfen ob in der Session schon Daten enthalten sind
        if not key in request.session: pass
        elif check_session_data(request, db_info, id, db, key):
            update_info = get_update_info(request, db_info)
            if update_info:
                try:
                    db.update_data(db_info, update_info, id = id)
                except Exception as ex:
                    context['warning'] = 'Die eingegebenen Daten waren fehlerhaft!'
                db.commit()
        else:
            if request.form:
                context['warning'] = 'Die Daten haben sich zwischenzeitlich geändert. Überprüfen Sie die Daten und senden sie Ihre Änderungen erneut.'

        # Daten aus der Datenbank holen
        row_data_dict = db.get_object(db_info, key = id)

    # Daten in der Session unter Schlüssel speichern
    request.session[key] = row_data_dict

    # Daten schreiben in context
    context.update({
        'row_data_dict': row_data_dict
    })

    # Letztendlich: An den Renderer schicken und in den Response laden
    return Response(render_func(context), content_type = "text/html")


def check_session_data(request, db_info, id, db, key):
    # aktuelle Daten aus der Datenbank holen und mit denen in der Session vergleichen
    row_data_dict = db.get_object(db_info, key = id)
    return request.session[key] == row_data_dict


def get_update_info(request, db_info):
    # Erzeugen eines Dictionary welches, die einzelnen Tabellespalten mit den Update-Daten enthält
    update_info = {}
    for item in request.form:
        if item in db_info['cols']:
            update_info[item] = request.form[item]
    return update_info


def customer_update_view(request):
    return update_view(request, get_default_context(request), config.DB_CUSTOMER, render_customer_update)

