from flask import Flask, jsonify, request
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
        "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.",
        "rating": 4
    },
    {
        "id": 5,
        "author": "Waldi Ravens",
        "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках.",
        "rating": 3
    },
    {
        "id": 6,
        "author": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.",
        "rating": 5
    },
    {
        "id": 8,
        "author": "Yoggi Berra",
        "text": "В теории, теория и практика неразделимы. На практике это не так.",
        "rating": 2
    }
]

def get_next_id():
    """Возвращает новый уникальный ID для цитаты."""
    if not quotes:
        return 1
    return quotes[-1]["id"] + 1

def validate_rating(rating):
    """Проверяет, что rating — целое число от 1 до 5. Если нет — возвращает 1."""
    if isinstance(rating, int) and 1 <= rating <= 5:
        return rating
    return 1

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/about")
def about():
    return about_me

@app.route("/quotes", methods=['GET'])
def get_quotes():
    return jsonify(quotes)

@app.route("/quotes", methods=['POST'])
def create_quote():
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Нет данных для отправки"}), 400
    if "author" not in data or "text" not in data:
        return jsonify({"error": "Незаполнены поля автора и текста"}), 400

    # Получаем rating, если передан, иначе — 1
    rating = data.get("rating", 1)
    rating = validate_rating(rating)

    new_id = get_next_id()
    new_quote = {
        "id": new_id,
        "author": data["author"],
        "text": data["text"],
        "rating": rating
    }
    quotes.append(new_quote)
    return jsonify(new_quote), 201

@app.route("/quotes/<int:quote_id>", methods=['GET'])
def get_quote_by_id(quote_id):
    for quote in quotes:
        if quote["id"] == quote_id:
            return jsonify(quote)
    return jsonify({"error": "Цитата не найдена"}), 404

@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Нет данных для обновления"}), 400

    for quote in quotes:
        if quote["id"] == quote_id:
            # Обновляем author и text, если переданы
            if "author" in data:
                quote["author"] = data["author"]
            if "text" in data:
                quote["text"] = data["text"]
            # Обновляем rating, если передан
            if "rating" in data:
                quote["rating"] = validate_rating(data["rating"])
            return jsonify(quote), 200

    return jsonify({"error": "Цитата не найдена"}), 404

@app.route("/quotes/<int:quote_id>", methods=['DELETE'])
def delete_quote(quote_id):
    for i, quote in enumerate(quotes):
        if quote["id"] == quote_id:
            quotes.pop(i)
            return jsonify({"message": f"Цитата с id {quote_id} удалена."}), 200
    return jsonify({"error": "Цитата не найдена"}), 404

@app.route("/quotes/count")
def get_quotes_count():
    return jsonify({"count": len(quotes)})

@app.route("/quotes/random")
def get_random_quote():
    if not quotes:
        return jsonify({"error": "Нет доступных цитат"}), 404
    random_quote = random.choice(quotes)
    return jsonify(random_quote)

@app.route("/quotes/filter", methods=['GET'])
def filter_quotes():
    # Получаем параметры запроса (author, rating и др.)
    author = request.args.get('author')
    rating = request.args.get('rating')

    # Начинаем с полного списка цитат
    filtered_quotes = quotes

    # Применяем фильтры, если параметры переданы
    if author:
        filtered_quotes = [q for q in filtered_quotes if q["author"] == author]

    if rating:
        # Преобразуем rating в число и проверяем корректность
        try:
            rating_val = int(rating)
            if 1 <= rating_val <= 5:
                filtered_quotes = [q for q in filtered_quotes if q["rating"] == rating_val]
        except (ValueError, TypeError):
            # Если rating не число — игнорируем фильтр
            pass

    # Если после фильтрации ничего не осталось — ошибка 404
    if not filtered_quotes:
        return jsonify({"error": "Цитаты не найдены по заданным фильтрам"}), 404

    return jsonify(filtered_quotes)

if __name__ == "__main__":
    app.run(debug=True)
