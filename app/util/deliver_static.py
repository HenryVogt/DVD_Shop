# -*- coding: utf-8 -*-
import os

from werkzeug.wrappers import Response, Request

import config
from error import Error404

def deliver_static(request):
    path_parts = request.path_args['filename'].split('/')
    
    path = os.path.join(config.STATIC_FILE_DIR, *path_parts)
    if os.path.isfile(path):
        response = Response(file(path).read())

        if '.' in path:
            suffix = path.split('.')[-1]
            if suffix in config.MIMETYPES:
                response.content_type = config.MIMETYPES[suffix]

        return response
    else:
        raise Error404('not found')

    