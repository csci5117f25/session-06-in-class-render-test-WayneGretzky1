
from flask import Flask, redirect, render_template, session, url_for, request, jsonify
import os
import json
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from db import setup, get_people, add_person


DATABASE_URL = os.environ['DATABASE_URL']
app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

with app.app_context():
    setup()



@app.route('/', methods=['GET'])
def home():
    user_name = request.args.get("userName", "unknown")
    return render_template('home.html', user=user_name) 


@app.route("/guestbook", methods=["GET"])
def show_guestbook():
    people = get_people()  # your DB query
    return render_template("guestbook.html", people=people)


@app.route("/guestbook", methods=["POST"])
def submit_guestbook():
    data = request.get_json()
    name = data.get("name")

    if name:
        add_person(name)
        return jsonify({"name": name}), 200
    else:
        return jsonify({"error": "Name is required"}), 400


@app.route("/guestbook/entries", methods=["GET"])
def get_guestbook_entries():
    people = get_people()
    formatted = [{"id": p[0], "name": p[1]} for p in people]
    return jsonify(formatted)






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