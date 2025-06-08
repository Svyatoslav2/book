from flask import Flask, request, jsonify
from book import recommend_books  # твоя функция из модуля book.py

app = Flask(__name__)

@app.route('/recommend', methods=['GET'])
def recommend():
    keywords = request.args.get('keywords', '')
    result = recommend_books(keywords)
    return jsonify({"recommendations": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

