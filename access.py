import requests
import json
import os
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient


g = open("CLIENT_ID")
c = open("TENANT_ID")
client_id = g.read().replace("\n", "")
tenant_id = c.read().replace("\n", "")
scopes = ['Sites.ReadWrite.All','Files.ReadWrite.All']
auth_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize'

oauth = OAuth2Session(client=MobileApplicationClient(client_id=client_id), scope=scopes)
authorization_url, state = oauth.authorization_url(auth_url)

consent_link = oauth.get(authorization_url)
os.system(f"xdg-open \"{consent_link.url}\"")
