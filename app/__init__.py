from flask import Flask
from config.database import db, init_db

def create_app():
    app = Flask(__name__)

    # Inicializa o banco de dados corretamente
    init_db(app)

    # Criar tabelas dentro do contexto da aplicação
    with app.app_context():
        db.create_all()

    # Importa e registra rotas dentro do contexto correto
    from app.routes.main import bp as main_bp
    from app.routes.users import bp as users_bp
    from app.routes.dumpsters import bp as dumpsters_bp
    from app.routes.reviews import bp as reviews_bp
    from app.routes.bookings import bp as bookings_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(dumpsters_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(bookings_bp)

    return app
