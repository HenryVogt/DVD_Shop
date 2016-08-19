# -*- coding: utf-8 -*-
from werkzeug.wrappers import Response, Request

from templates.error_view_renderer import render

def error404_view(request):
    context = {
        'title': 'Error404',
        'message': request.error404_msg,
        'root_path': request.script_root_ext
    }

    response = Response(render(context), content_type="text/html")
    response.status = "404 Not Found"
    response.status_code = 404

    return response

