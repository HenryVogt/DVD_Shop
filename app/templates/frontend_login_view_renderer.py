# -*- coding: utf-8 -*-
from templates import templates as tpl


def render(context):

    content = tpl['frontend_login']

    context['flash_info'] = ""
    context['navigation_items'] = ""
    context['section_title'] = "Login"
    context['searchfield'] = ""

    return tpl['base'].format(content = content, **context).format(**context)


