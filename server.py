
from flask import Flask, redirect, render_template, session, url_for, request
import os
import json
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from db import setup


app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

def initialize_db():
    setup()

@app.route('/', methods=['GET'])
def main():
    user_name = request.args.get("userName", "unknown")
    return render_template('main.html', user=user_name) 


@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    return render_template('guestbook.html') 






# Auth stuff
# sub is our id, technically, use it as userid, name given name, email, picture

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + os.environ.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("hello", _external=True),
                "client_id": os.environ.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


if __name__ == "__main__":
    app.run(debug=True)
# pipenv run flask --app server.py run