from flask import Flask, jsonify
import random

app = Flask(__name__)
app.json.ensure_ascii = False

about_me = {
    "name": "Алексей",
    "surname": "Геннадьевич",
    "lastname": "Косенко",
    "email": "cuctemarma@vk.com"
}

quotes = [
    {
        "id": 3,
        "author": "Rick Cook",
        "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
    },
    {
        "id": 5,
        "author": "Waldi Ravens",
        "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
    },
    {
        "id": 6,
        "author": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
    },
    {
        "id": 8,
        "author": "Yoggi Berra",
        "text": "В теории, теория и практика неразделимы. На практике это не так."
    }
]
# Нужно больше цитат? https://tproger.ru/devnull/programming-quotes/


@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/about")
def about():
    return about_me

@app.route("/quotes")
def get_quotes():
    return jsonify(quotes)

@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    # Ищем цитату с заданным id
    for quote in quotes:
        if quote["id"] == quote_id:
            return jsonify(quote)  # Возвращаем найденную цитату
    
    # Если цитата не найдена — возвращаем ошибку 404
    return jsonify({"error": "Цитата не найдена"}), 404

@app.route("/quotes/count")
def get_quotes_count():
    count = len(quotes)  # Считаем количество цитат
    return jsonify({"count": count})  # Возвращаем JSON с ключом "count"

@app.route("/quotes/random")
def get_random_quote():
    random_quote = random.choice(quotes)  # Выбираем случайную цитату
    return jsonify(random_quote)  # Возвращаем её в формате JSON

if __name__ == "__main__":
    app.run(debug=True)
