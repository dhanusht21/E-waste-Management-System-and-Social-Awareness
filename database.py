import sqlite3

conn = sqlite3.connect('ewaste.db')
c = conn.cursor()

# EXISTING TABLES (keep them)
c.execute("""
CREATE TABLE IF NOT EXISTS ewaste (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    item TEXT,
    category TEXT,
    request_type TEXT,
    status TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# 🔥 NEW TABLES (ADD THIS)
c.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")

# DEFAULT ADMIN
c.execute("""
INSERT OR IGNORE INTO users (id, username, password, role)
VALUES (1, 'admin', 'admin@123', 'admin')
""")

# DEFAULT CATEGORIES
categories = ['Mobile', 'Laptop', 'Battery', 'Monitor', 'Printer']
for cat in categories:
    c.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))

# DEFAULT ITEMS
items = ['Old Mobile Phone', 'Laptop Charger', 'CRT Monitor', 'Ink Printer', 'Power Bank']
for item in items:
    c.execute("INSERT OR IGNORE INTO items (name) VALUES (?)", (item,))

conn.commit()
conn.close()

print("Database initialized successfully")
