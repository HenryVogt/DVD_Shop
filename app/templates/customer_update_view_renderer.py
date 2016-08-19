# -*- coding: utf-8 -*-

from templates import templates as tpl
from navigation_renderer import render as render_navigation

def render(context):
    # Mit Customer-Templates rendern
    context['update_body'] = tpl['customer_update_form'].format(customer=context['row_data_dict'], **context)
    context['subpage_title'] = tpl['customer_update_heading'].format(customer=context['row_data_dict'])
    context['navigation_items'] = render_navigation(context)
    context['flash_info'] = ""
    if 'warning' in context:
        context['flash_info'] = tpl['flash_info'].format(warning=context['warning'])

    return tpl['base'].format(content = tpl['update_details'], **context).format(**context)
