# authcord.py
A Python module used for interacting with Discord's OAuth API. Can be used with any Python web framework.

**NOTE:** *This module was made for internal use on some of my projects, this might make it hard to implement into your own. Feel free to tweak the source code as you please, just make sure to include the License! :)*

Documentation coming soon!


## Example

This example uses every feature of [authcord.py](https://github.com/IreTheKID/authcord.py/blob/main/authcord/__init__.py)! Run it on [Repl.it](https://repl.it/@IreTheKID/Authcord-Example#main.py)!

```python
import os
import flask

app = flask.Flask(__name__)

# Initialize vars BEFORE importing authcord
os.environ["TOKEN"]         = "web application token"
os.environ["SCOPES"]        = "identify email"
os.environ["CLIENT_ID"]     = "client id here"
os.environ["CLIENT_SECRET"] = "client secret here"
os.environ["REDIRECT_URI"]  = "redirect uri here"

import authcord

@app.route("/")
def index():
    return "Hello!"

@app.route("/login-discord")
def login_discord():
    state = authcord.create_state({"password" : "1234"}, 5)
    request_uri = authcord.get_request_uri(state=state)
    
    return flask.redirect(request_uri)

@app.route("/login-discord/callback")
def login_callback():
    raw_state = flask.request.args.get("state")
    state = authcord.parse_state(raw_state)
    
    if not state:
        return flask.abort(403)
    else:
        code = flask.request.args.get("code")
        token = authcord.parse_token(authcord.exchange_code(code))
        
        user = authcord.access_endpoint("/users/@me", "GET", "Bearer", token["access_token"])
        
        return f"Here's your Discord Info:<br>{user}"

app.run(host="0.0.0.0", port=8080)
```
