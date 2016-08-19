# -*- coding: utf-8 -*-
from templates import templates as tpl
from detail_view_renderer import render as render_detail_view

def render(context):
    # Mit Customer-Templates rendern
    context['details_tbody'] = tpl['product_details'].format(product=context['detail_data_dict'], **context)
    context['subpage_title'] = tpl['product_details_heading'].format(product=context['detail_data_dict'])

    if 'detail_list_dict' in context:
        context['details_list'] = "\n".join([tpl['order_details_list'].format(orderlines = orderlines, **context) for orderlines in context['detail_list_dict']])
    else:
        context['details_list'] = ""

    # Detail wie gewohnt rendern
    return render_detail_view(context)

