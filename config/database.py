from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Criamos uma única instância global do SQLAlchemy

def init_db(app):
    """Inicializa o banco de dados e vincula ao app Flask"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/aluguel_cacambas'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Inicializa o banco de dados no contexto do Flask
