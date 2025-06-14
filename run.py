from app import create_app
from config.database import db

def testar_conexao_banco(app):
    with app.app_context():
        try:
            # Tenta abrir uma conexão com o banco
            with db.engine.connect() as conn:
                print("✅ Conexão com o banco de dados bem-sucedida.")
        except Exception as e:
            print(f"❌ Falha ao conectar com o banco de dados: {e}")
            exit(1)

# Cria o app e testa a conexão

app = create_app()  # Agora o app é criado corretamente

if __name__ == "__main__":
    app.run(debug=True)
