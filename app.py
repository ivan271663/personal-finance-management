from flask import Flask
from database import init_db
from routes import setup_routes

app = Flask(__name__)

# Инициализируем базу данных
init_db()

# Настраиваем маршруты
setup_routes(app)

if __name__ == '__main__':
    app.run(debug=True)