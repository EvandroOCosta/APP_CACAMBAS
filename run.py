from flask import Flask
from app.routes import users, dumpsters, bookings, reviews, main

# Inicializando o app Flask
app = Flask(__name__)

# Registro de rotas
app.register_blueprint(main.bp)
app.register_blueprint(users.bp)
app.register_blueprint(dumpsters.bp)
app.register_blueprint(bookings.bp)
app.register_blueprint(reviews.bp)

if __name__ == "__main__":
    app.run(debug=True)
