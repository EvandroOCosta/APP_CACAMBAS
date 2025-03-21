from flask import Flask
from config.database import db, init_db

def create_app():
    app = Flask(__name__)

    # Inicializa o banco de dados corretamente
    init_db(app)

    with app.app_context():
        db.create_all()  # Cria as tabelas dentro do contexto correto

    # Importa e registra rotas dentro do contexto correto
    from app.routes.users import bp as users_bp
    app.register_blueprint(users_bp)

    return app
