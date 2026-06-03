import sqlite3
from pathlib import Path

print(sqlite3.sqlite_version)


dp_path = Path("docs/temp.db")
dp_path.parent.mkdir(exist_ok=True)
conn = sqlite3.connect(str(dp_path))
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    )
    """
)

cursor.execute(
    "INSERT INTO users (username, password) Values(?, ?)",
    ("admin", "admin")
)

conn.commit()

cursor.execute("SELECT *  FROM users")
users = cursor.fetchall()
for user in users:
    print(user)

conn.close()


















