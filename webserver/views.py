from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import requests
from dotenv import load_dotenv
import os

load_dotenv()


views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():

    # api call to check geo info based on ip
    client_ip = request.remote_addr
    print(f"client_ip: {client_ip}")
    ipbase_api_acesskey = os.environ.get("IPBASE_API_TOKEN")
    api_url = f"https://api.ipbase.com/v2/info?ip={client_ip}&apikey={ipbase_api_acesskey}"
    api_response = requests.get(api_url)
    api_response = api_response.json()
    print(f"api_response: {api_response}")

    return render_template("home.html", user=current_user)
