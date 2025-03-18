from flask import Flask
from config.database import init_db, db

def create_app():
    app = Flask(__name__)

    # Inicializar banco de dados
    init_db(app)

    return app
