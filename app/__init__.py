from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuração do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Altere se seu usuário não for root
app.config['MYSQL_PASSWORD'] = 'sua_senha'  # Substitua pela senha do seu MySQL
app.config['MYSQL_DB'] = 'aluguel_cacambas'  # Nome do banco de dados

# Inicializar a conexão com o MySQL
mysql = MySQL(app)

