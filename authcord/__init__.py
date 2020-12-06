import os
import json
import requests

from oauthlib.oauth2 import WebApplicationClient
from itsdangerous import TimedJSONWebSignatureSerializer as JWS

API_ENDPOINT = "https://discord.com/api/v8"
IMG_BASE = "https://cdn.discordapp.com/avatars/{0}/{1}.png?size={2}"

TOKEN = os.environ["TOKEN"]
SCOPES = os.environ["SCOPES"].split(" ")
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

client = WebApplicationClient(CLIENT_ID)


def create_state(payload: dict, expiration: int):
    s = JWS(TOKEN, expiration * 60)
    raw_state = s.dumps(payload).decode("utf-8")

    return raw_state


def parse_state(raw_state: str):
    s = JWS(TOKEN)
    try:
        state = s.loads(raw_state)
        return state
    except:
        return None


def get_request_uri(state=None):
    uri = client.prepare_request_uri(
        "https://discord.com/api/oauth2/authorize",
        redirect_uri=os.environ["REDIRECT_URI"],
        scope=SCOPES,
        state=state,
    )
    return uri


def exchange_code(code: str):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.environ["REDIRECT_URI"],
        "scope": "identify",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    r = requests.post(
        "https://discord.com/api/v8/oauth2/token", data=data, headers=headers
    )
    r.raise_for_status()
    return r.json()


def parse_token(token_json: dict):
    parsed = client.parse_request_body_response(json.dumps(token_json))
    return parsed


def access_endpoint(endpoint, method, ttype="", token="", data=None):
    head = {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Authorization": f"{ttype} {token}" if ttype else "",
    }

    r = requests.request(method, f"{API_ENDPOINT}{endpoint}", headers=head, data=data)

    r.raise_for_status()
    return r.json()
