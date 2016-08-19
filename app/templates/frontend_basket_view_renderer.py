# -*- coding: utf-8 -*-
from templates import templates as tpl
from frontend_list_view_renderer import render as render_list_view

from navigation_renderer import render as render_navigation

def render(context):
    # Head und Zeilen der Liste mit Customer-Templates rendern
    context['list_rows'] = "\n".join([tpl['frontend_basket_list_row'].format(product = product, **context) for product in context['list_data_dict']])
    context['list_head'] = tpl['frontend_basket_list_head']
    
    pagination_back_link = tpl['pagination_back'].format(page = str(context['page'] - 1), href = "/".join([context['root_path'], context['section_path'], 'seite', str(context['page'] - 1), context["queryPath"]])) if  context['page'] > 1 else ""
    pagination_forward_link = tpl['pagination_forward'].format(page = str(context['page'] + 1), href = "/".join([context['root_path'], context['section_path'], 'seite', str(context['page'] + 1), context["queryPath"]])) if  context['pages_to_come'] > 0 else ""
    
    context['pagination'] = tpl['pagination'].format(back_link = pagination_back_link, forward_link = pagination_forward_link)

    context['navigation_items'] = render_navigation(context)
    context['list'] = tpl['list'].format(**context)
    context['searchfield'] = ""

    # Liste wie gewohnt rendern
    return tpl['base'].format(content = tpl['frontend_basket'], **context).format(**context)


