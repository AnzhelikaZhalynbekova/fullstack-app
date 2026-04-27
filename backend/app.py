from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")


# 🔹 Подключение к БД
def get_conn():
    return psycopg2.connect(DATABASE_URL)


# 🔥 Авто-создание таблицы
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


# 🔹 GET
@app.route("/api/data", methods=["GET"])
def get_data():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM items;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    # превращаем в нормальный JSON
    result = [{"id": r[0], "name": r[1]} for r in rows]

    return jsonify(result)


# 🔹 POST
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

    return jsonify({
        "message": "Item added",
        "id": new_id
    }), 201


# 🔹 DELETE
@app.route("/api/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM items WHERE id = %s;", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"status": "deleted"})


# 🚀 ВАЖНО: запуск
if __name__ == "__main__":
    init_db()  # ← ВОТ ЗДЕСЬ вызываем
    app.run(host="0.0.0.0", port=5001)