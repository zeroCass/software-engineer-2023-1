from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    """ define the app object, routes and database connection """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "my_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    # define the database
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import Estudante, Professor, Matricula, Turma, Presenca
    with app.app_context():
        db.create_all()
        # seed_database()
        professores = Professor.query.all()
        for professor in professores:
            print(professor.matricula, professor.senha)

    # login_manager.user_loader
    @login_manager.user_loader
    def load_user(id):
        return Professor.query.get(int(id)) or Estudante.query.get(int(id))

    return app


def seed_database():
    from .models import Estudante, Professor, Matricula, Turma, Presenca
    # create some datas
    prof = Professor(nome="Alberto Dores", matricula="00001",
                     email="professor1@email.com", senha="123")
    db.session.add(prof)
    db.session.commit()

    estudante = Estudante(nome="Joao das Neves", matricula="00002",
                          email="estudante1@email.com", senha="123")
    turma = Turma(nome="Engenharia de Software",
                  horario="Ter e Qui - 08h as 10h", semestre="sexto", professor_id=prof.id)

    db.session.add_all([estudante, turma])
    db.session.commit()
