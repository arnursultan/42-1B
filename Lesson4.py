# INTEGER — Целое число
# REAL — Дробное число
# TEXT — Строка
# BLOB — Бинарные данные (файлы, картинки)
#
# import sqlite3
#
# CREATE TABLE servers (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     type TEXT NOT NULL,
#     status TEXT DEFAULT "жив",
#     file_data BLOB,
#     file_name TEXT,
#     file_type TEXT
# )
#
# CREATE TABLE backup_server (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     description TEXT NOT NULL,
#     server_id INTEGER,
#     FOREIGN KEY (server_id) REFERENCES servers (id)
# )


CREATE TABLE servers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    status text DEFAULT 'на чилле'
);

CREATE TABLE incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    server_id INTEGER,
    FOREIGN KEY (server_id) REFERENCES servers (id)
);


INSERT INTO servers (name, type, status) VALUES ('web_server', 'web', 'на расслабоне');
INSERT INTO servers (name, type, status) VALUES ('db_server', 'db', 'работает');

INSERT INTO incidents (description, server_id) VALUES ('диск заполнен на 99%', 2)

.tables — список таблиц в базе
.schema servers — структура конкретной таблицы
.mode column — красивый вывод таблицами
.headers on — показывать названия столбцов