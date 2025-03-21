from app import create_app
from config.database import db

app = create_app()

with app.app_context():
    print("Verificando conexão com o banco de dados...")

    # Testa a conexão com o MySQL
    try:
        with db.engine.connect() as connection:
            print("✅ Conexão bem-sucedida com o MySQL!")
    except Exception as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        exit()

    print("Apagando tabelas existentes...")
    db.drop_all()  # Apaga todas as tabelas (se existirem)
    print("Criando novas tabelas...")
    db.create_all()  # Cria as tabelas do zero
    print("✅ Tabelas criadas com sucesso!")
