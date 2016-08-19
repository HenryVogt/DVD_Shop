# -*- coding: utf-8 -*-
from templates import templates as tpl

from navigation_renderer import render as render_navigation

def render(context):
	context['navigation_items'] = render_navigation(context)
	return tpl['base'].format(content = tpl['search_form'], **context).format(**context)

def render_customer(context):
	context['search_form_items'] = tpl['search_form_items_customer'].format(**context)
	return render(context)

def render_product(context):
	context['search_form_items'] = tpl['search_form_items_product'].format(**context)
	return render(context)

def render_order(context):
	context['search_form_items'] = tpl['search_form_items_order'].format(**context)
	return render(context)
    


