import sqlite3

import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('simple_poop.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Score (
id INTEGER PRIMARY KEY,
first_name TEXT NOT NULL UNIQUE,
username TEXT NOT NULL UNIQUE,
score INTEGER
)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()