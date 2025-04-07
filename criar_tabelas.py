from app import create_app
from config.database import db

# 🔄 Importa os modelos para que SQLAlchemy os reconheça
from app.models.user import User
from app.models.booking import Booking
from app.models.review import Review
from app.models.dumpster import Dumpster


app = create_app()

with app.app_context():
    print("Verificando conexão com o banco de dados...")

    try:
        with db.engine.connect() as connection:
            print("✅ Conexão bem-sucedida com o MySQL!")
    except Exception as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        exit()

    print("Apagando tabelas existentes...")
    db.drop_all()

    print("Criando novas tabelas...")
    db.create_all()

    print("✅ Tabelas criadas com sucesso!")
