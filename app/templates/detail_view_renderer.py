# -*- coding: utf-8 -*-
from templates import templates as tpl

from navigation_renderer import render as render_navigation

def render(context):

    context['navigation_items'] = render_navigation(context)
    context['flash_info'] = ""

    return tpl['base'].format(content = tpl['details'], **context).format(**context)