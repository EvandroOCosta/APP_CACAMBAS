from app import create_app

app = create_app()  # Agora o app é criado corretamente

if __name__ == "__main__":
    app.run(debug=True)
