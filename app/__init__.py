from flask import Flask
from config.database import init_db, mysql

def create_app():
    app = Flask(__name__)

    # Configurar banco de dados
    init_db(app)

    return app