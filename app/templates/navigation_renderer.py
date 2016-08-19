# -*- coding: utf-8 -*-
from templates import templates as tpl

def render(context):

    return "".join([
        tpl['navigation_item'].format(
            name = item['name'], 
            href = "/".join([
                context['root_path'], item['path']
            ]),
            active = "active" if item['path'] == context['section_path'] else ""
        ) for item in context['navigation']
    ])