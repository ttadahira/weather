#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgitb
cgitb.enable()

from wsgiref.handlers import CGIHandler
from weather_short import app

class ProxyFix(object):
  def __init__(self, app):
      self.app = app
  def __call__(self, environ, start_response):
      # ※要書き換え
      environ['SERVER_NAME'] = "153.121.39.165"
      environ['SERVER_PORT'] = "80"
      environ['SERVER_PROTOCOL'] = "HTTP/1.1"
      return self.app(environ, start_response)

if __name__ == '__main__':
   app.wsgi_app = ProxyFix(app.wsgi_app)
   CGIHandler().run(app)