# -*- coding: utf-8 -*-
import config

def get_default_context(request):

    path = request.path_args['path']

    context = {
        'title': config.APP_NAME,
        'navigation': config.NAVIGATION,
        'section_path': path[0],
        'subpage_path': "/".join(path),
        'root_path': request.script_root_ext,
        'flash_info': "",
        'searchfield': "",
        'search_str': ""        
    }

    for section in config.NAVIGATION:
        if path[0] == section['path']:
            context['section_title'] = section['name']

    return context

def get_default_context_frontend(request):

    path = request.path_args['path']

    context = {
        'title': config.APP_NAME_ORDER,
        'navigation': config.NAVIGATION_ORDER,
        'section_path': path[0],
        'subpage_path': "/".join(path),
        'root_path': request.script_root_ext,
        'flash_info': "",
        'searchfield': "",
        'search_str': ""
    }

    for section in config.NAVIGATION_ORDER:
        if path[0] == section['path']:
            context['section_title'] = section['name']

    return context