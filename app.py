from flask import Flask
from database.connection import get_db_connection

app = Flask(__name__)

try:
    conn = get_db_connection()
    print("✅ Database connected successfully.")
    conn.close()
except Exception as e:
    print("❌ Database connection failed.")
    print(e)


@app.route("/")
def home():
    return "BelajarYuk is running!"


if __name__ == "__main__":
    app.run(debug=True)