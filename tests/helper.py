import requests

import os
HOST = os.environ.get("APP_HOST", "0.0.0.0")

def req(method: str, endpoint: str, body=None):
  url = f"http://{HOST}:3193{endpoint}"
  res = requests.request(
    method = method,
    url    = url,
    json   = body,
  )
  return (res.status_code, res.json())

def print_state():
  print(req('GET', '/state'))
