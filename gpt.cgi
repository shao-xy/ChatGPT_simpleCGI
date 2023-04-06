#!/usr/bin/env python3

API_KEY = ''

COMMON_HTML_HEADER = 'Content-type: text/html\n\n'
COMMON_JSON_HEADER = 'Content-type: application/json\n\n'
COMMON_RESPONSE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>OK!</title>
</head>
<body>
</body>
</html>
"""
import sys
import os

import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
#print(COMMON_HTML_HEADER)
#sys.stdout.flush()

import json

import cgi
import cgitb
cgitb.enable(display=1, logdir=os.path.join(os.path.dirname(sys.argv[0]), 'log'))

sys.path.insert(0, '/home/ecs-user/openai/ChatGPT_cli/')
from openai_chatter import Chatter

def parse_args():
  cookies = None
  if 'HTTP_COOKIE' in os.environ:
      cookie_string = os.environ.get('HTTP_COOKIE')
      c = Cookie.SimpleCookie()
      c.load(cookie_string)
      cookies = { k: c[k].value for k in c.keys() }

  cgi_storage = cgi.FieldStorage()
  cgidata = { k: cgi_storage.getvalue(k) for k in cgi_storage.keys() }

  remote_addr = 'REMOTE_ADDR' in os.environ and os.environ['REMOTE_ADDR'] or ''
  return cookies, cgidata, remote_addr

def main():
  cookies, cgidata, remote_addr = parse_args()
  prompt = 'p' in cgidata and cgidata['p'] or ''
  if not prompt:
    print(COMMON_JSON_HEADER)
    print(json.dumps({'success': 0, 'msg': ''}))
    return 0

  chatter = Chatter(API_KEY)
  response_dict = {'success': 1, 'msg': chatter.interact(prompt)}
  print(COMMON_JSON_HEADER)
  print(json.dumps(response_dict))

  return 0

if __name__ == '__main__':
  sys.exit(main())
