from flask import Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

about_me = {
    "name": "Алексей",
    "surname": "Геннадьевич",
    "lastname": "Косенко",
    "email": "cuctemarma@vk.com"
}

@app.route("/")  # Это первый URL, который мы будем обрабатывать
def hello_world():  # Это функция-обработчик будет вызвана при запросе этого URL.
    return "Hello, World!"

@app.route("/about")
def about():
    return about_me


if __name__ == "__main__":
    app.run(debug=True)

