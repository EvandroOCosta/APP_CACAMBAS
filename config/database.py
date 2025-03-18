#from flask_mysql_connector import MySQL
from flask_mysqldb import MySQL


mysql = MySQL()

def init_db(app):
    """Inicializa o banco de dados no Flask"""
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'  # Altere se necessário
    app.config['MYSQL_PASSWORD'] = 'sua_senha'  # Substitua pela senha correta
    app.config['MYSQL_DB'] = 'aluguel_cacambas'

    mysql.init_app(app)
