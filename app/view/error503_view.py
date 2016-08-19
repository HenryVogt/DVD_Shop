# -*- coding: utf-8 -*-
from werkzeug.wrappers import Response, Request

from templates.error_view_renderer import render

def error503_view(request):
    context = {
        'title': 'Error503',
        'message': request.error503_msg,
        'root_path': request.script_root_ext
    }

    response = Response(render(context), content_type="text/html")
    response.status = "503 Service Unavailable"
    response.status_code = 503

    return response

