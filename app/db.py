import sqlite3
from .config import DB_PATH
from werkzeug.security import generate_password_hash
from datetime import date, timedelta


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

    # Seed minimal data if missing so login works out-of-the-box
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO users (username,password_hash,display_name) VALUES (?,?,?)",
                    ("admin", generate_password_hash("admin123"), "Admin"))
    cur.execute("SELECT COUNT(*) FROM artists")
    if cur.fetchone()[0] == 0:
        sample_artists = ["Trio Lumina", "DJ Faro", "Compagnia Nova"]
        for a in sample_artists:
            cur.execute("INSERT OR IGNORE INTO artists (name) VALUES (?)", (a,))
    cur.execute("SELECT COUNT(*) FROM formats")
    if cur.fetchone()[0] == 0:
        sample_formats = ["Concerto", "Spettacolo Teatrale", "DJ Set"]
        for f in sample_formats:
            cur.execute("INSERT OR IGNORE INTO formats (name) VALUES (?)", (f,))
    cur.execute("SELECT COUNT(*) FROM people")
    if cur.fetchone()[0] == 0:
        sample_people = [
            ("PromoterOne","PROMOTER"),
            ("Mario Rossi","TOUR_MANAGER"),
            ("Luca B","VOCALIST"),
            ("MascotteMax","MASCOT"),
            ("BellaDanse","BALLERINA"),
            ("ServiceX","SERVICE_IMPIANTI"),
        ]
        for name, role in sample_people:
            cur.execute("INSERT OR IGNORE INTO people (name, role) VALUES (?,?)", (name, role))
    cur.execute("SELECT COUNT(*) FROM events")
    if cur.fetchone()[0] == 0:
        today = date.today()
        events = [
            ("Apertura Stagione", today.isoformat(), 1, 1, "Evento inaugurale"),
            ("Festa DJ Faro", (today + timedelta(days=3)).isoformat(), 3, 1, "DJ set all'aperto"),
            ("Compagnia Nova - prova", (today + timedelta(days=7)).isoformat(), 2, 1, "Prova generale"),
        ]
        for title, d, fmt, promoter, notes in events:
            cur.execute("INSERT OR IGNORE INTO events (title,date,format_id,promoter_id,notes) VALUES (?,?,?,?,?)",
                        (title, d, fmt, promoter, notes))
        cur.execute("SELECT id FROM events")
        event_ids = [r[0] for r in cur.fetchall()]
        if event_ids:
            cur.execute("INSERT OR IGNORE INTO event_artists (event_id, artist_id) VALUES (?,?)", (event_ids[0], 1))
            if len(event_ids) > 1:
                cur.execute("INSERT OR IGNORE INTO event_artists (event_id, artist_id) VALUES (?,?)", (event_ids[1], 2))
            if len(event_ids) > 2:
                cur.execute("INSERT OR IGNORE INTO event_artists (event_id, artist_id) VALUES (?,?)", (event_ids[2], 3))
    conn.commit()
    conn.close()
