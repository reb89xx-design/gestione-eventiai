import sqlite3
from .config import DB_PATH

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password_hash TEXT,
        display_name TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS formats (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        title TEXT,
        date TEXT,
        format_id INTEGER,
        promoter_id INTEGER,
        notes TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS event_artists (
        event_id INTEGER,
        artist_id INTEGER,
        PRIMARY KEY (event_id, artist_id)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS event_people (
        event_id INTEGER,
        person_id INTEGER,
        role TEXT,
        PRIMARY KEY (event_id, person_id, role)
    )""")
    conn.commit()
    conn.close()
