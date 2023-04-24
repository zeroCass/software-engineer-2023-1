from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Estudante, Professor
from flask_login import login_user, login_required, logout_user, current_user
import requests
import os
from dotenv import load_dotenv


load_dotenv()

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        matricula = request.form.get("matricula")
        password = request.form.get("senha")
        print(f"dados recebidos: {matricula}, {password}")

        user = Professor.query.filter_by(matricula=matricula).first(
        ) or Estudante.query.filter_by(matricula=matricula).first()
        if user:
            print("Usuario existe", user)
            if user.senha == password:
                flash("Logado com sucesso!", category="sucess")
                # make user loggin
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Senha invalida!", category="error")
        flash("Usuario nao existe!", category="error")
        print("Usuario nao existe!")

    return render_template("login.html", user=current_user)


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        matricula = request.form.get("matricula")
        senha = request.form.get("senha")
        account_type = request.form.get("account-type")

        # check if email is valid with api
        hunter_api_acesskey = os.environ.get("HUNTER_API_TOKEN")
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={hunter_api_acesskey}"
        api_response = requests.get(url)
        api_response = api_response.json()

        if api_response["data"]["status"] == "valid":
            new_user = ''
            if account_type == "professor":
                new_user = Professor(matricula=matricula,
                                     email=email, nome=nome, senha=senha)
            if account_type == "estudante":
                new_user = Estudante(matricula=matricula,
                                     email=email, nome=nome, senha=senha)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Usuario Cadastrado com sucesso!")
                login_user(new_user, remember=True)
                return redirect(url_for("views.home"))
            except Exception:
                db.session.rollback()
                flash("Erro ao cadastrar usuario: matricula ou email ja cadastrados.")
        else:
            flash("O email fornecido nao eh valido!")

    return render_template("signin.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
