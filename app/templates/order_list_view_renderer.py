# -*- coding: utf-8 -*-
from templates import templates as tpl
from list_view_renderer import render as render_list_view

def render(context):
    # Head und Zeilen der Liste mit Customer-Templates rendern
    context['list_rows'] = "\n".join([tpl['order_list_row'].format(order = order, **context) for order in context['list_data_dict']])
    context['list_head'] = tpl['order_list_head']
    context['searchfield'] = tpl['search_field']
    # Liste wie gewohnt rendern
    return render_list_view(context)


