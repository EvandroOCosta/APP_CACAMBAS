from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Inicializa o banco de dados no Flask com SQLAlchemy"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/aluguel_cacambas'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sua_senha@localhost/aluguel_cacambas'


    db.init_app(app)
