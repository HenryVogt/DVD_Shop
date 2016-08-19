# -*- coding: utf-8 -*-

class Error404(Exception):
    def __init__(self, msg):
        self.msg = msg

class Error503(Exception):
    def __init__(self, msg):
        self.msg = msg