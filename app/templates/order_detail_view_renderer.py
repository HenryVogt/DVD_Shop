# -*- coding: utf-8 -*-
from templates import templates as tpl
from detail_view_renderer import render as render_detail_view

def render(context):
    # Mit Customer-Templates rendern
    context['details_tbody'] = tpl['order_details'].format(order=context['detail_data_dict'], **context)
    context['subpage_title'] = tpl['order_details_heading'].format(order=context['detail_data_dict'])

    if 'detail_list_dict' in context:
        context['details_list_row'] = "\n".join([tpl['order_details_list_row'].format(orderlines = orderlines, **context) for orderlines in context['detail_list_dict']])
    else:
        context['details_list_row'] = ""

    context['details_list'] = tpl['order_details_list_head'].format(**context)

    # Detail wie gewohnt rendern
    return render_detail_view(context)


