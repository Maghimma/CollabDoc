import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/token')
def generate_token():
    TWILLIO_ACCOUNT_SID = 'AC2f3a39af2e9058810b4b4f02516d4346'
    TWILLIO_SYNC_SERVICE_SID = 'IS01f646d8e91480c9e083795fc51abfc1'
    TWILLIO_API_KEY = 'SK852503d262a07f249836c6490ef6e4a0'
    TWILLIO_API_SECRET = 'UOG8hsR7IvjEs3yZlLQcGo20WoyRLLz9'

    username = request.args.get('username', fake.user_name())

    token = AccessToken(TWILLIO_ACCOUNT_SID, TWILLIO_API_KEY, TWILLIO_API_SECRET, identity=username)
    sync_grant_access = SyncGrant(TWILLIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad = request.form['text']
    with open('workfile.txt', 'w') as f: 
        f.write(text_from_notepad)

    path_to_store_txt = "workfile.txt"

    return send_file(path_to_store_txt, as_attachment=True)  

if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
