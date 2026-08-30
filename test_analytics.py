import sys
import os
import json
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError

def login():
    url = 'http://127.0.0.1:8000/auth/login'
    data = json.dumps({"email": "official@policygpt.gov.in", "password": "Password123"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req) as f:
            resp = json.loads(f.read().decode('utf-8'))
            return resp.get('access_token')
    except HTTPError as e:
        print(f"Login failed: {e.code} {e.read().decode('utf-8')}")
        sys.exit(1)
    except URLError as e:
        print(f"Server not reachable: {e.reason}")
        sys.exit(1)

def get_analytics(token):
    url = 'http://127.0.0.1:8000/analytics/overview'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'}, method='GET')
    try:
        with urllib.request.urlopen(req) as f:
            resp = json.loads(f.read().decode('utf-8'))
            print("Successfully fetched analytics. Keys in response:")
            for k in resp.keys():
                print(f"- {k}")
            print("\nMetrics:")
            print(json.dumps(resp.get('metrics', {}), indent=2))
    except HTTPError as e:
        print(f"Analytics failed: {e.code} {e.read().decode('utf-8')}")
    except URLError as e:
        print(f"Server not reachable: {e.reason}")

if __name__ == '__main__':
    token = login()
    if token:
        get_analytics(token)
