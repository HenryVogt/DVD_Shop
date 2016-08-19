# -*- coding: utf-8 -*-
from templates import templates as tpl

from navigation_renderer import render as render_navigation

def render(context):
    pagination_back_link = tpl['pagination_back'].format(page = str(context['page'] - 1), href = "/".join([context['root_path'], context['section_path'], 'seite', str(context['page'] - 1), context["query_path"]])) if  context['page'] > 1 else ""
    pagination_forward_link = tpl['pagination_forward'].format(page = str(context['page'] + 1), href = "/".join([context['root_path'], context['section_path'], 'seite', str(context['page'] + 1), context["query_path"]])) if  context['pages_to_come'] > 0 else ""
    
    context['pagination'] = tpl['pagination'].format(back_link = pagination_back_link, forward_link = pagination_forward_link)
    context['navigation_items'] = render_navigation(context)
    context['flash_info'] = ""
    
    return tpl['base'].format(content = tpl['list'], **context).format(**context)