from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")


# 🔹 Подключение к БД
def get_conn():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL is missing")
    return psycopg2.connect(DATABASE_URL)


# 🔥 Создание таблицы (БЕЗ авто-вызова при import)
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


@app.route("/api/data", methods=["GET"])
def get_data():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM items;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([{"id": r[0], "name": r[1]} for r in rows])


@app.route("/api/data", methods=["POST"])
def add_data():
    data = request.json

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO items (name) VALUES (%s) RETURNING id;",
        (data["name"],)
    )

    new_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_id}), 201


@app.route("/api/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM items WHERE id = %s;", (id,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "deleted"})


# 🚀 Railway-safe start
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    # создаём таблицу ТОЛЬКО при запуске сервера
    init_db()

    app.run(host="0.0.0.0", port=port)