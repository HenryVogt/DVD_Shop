# -*- coding: utf-8 -*-
from templates import templates as tpl

def render(context):

    return tpl['error'].format(**context)