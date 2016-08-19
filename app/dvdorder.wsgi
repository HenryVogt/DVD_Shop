#!/usr/bin/python
#-*- coding: utf-8 -*-
import os, sys
reload(sys)
sys.setdefaultencoding("utf-8")

from werkzeug.wrappers import Response, Request
import werkzeug.contrib.sessions as sessions

sys.path.append(os.path.dirname(__file__))

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

from dvdorder import application 

fsstore = sessions.FilesystemSessionStore()
application = sessions.SessionMiddleware(application,fsstore)

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 8080, application, use_reloader=True, use_debugger=True)
