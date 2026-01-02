from app.db import init_db, get_conn
from werkzeug.security import generate_password_hash
from datetime import date, timedelta

def seed():
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO users (username,password_hash,display_name) VALUES (?,?,?)",
                    ("admin", generate_password_hash("admin123"), "Admin"))
    cur.execute("SELECT COUNT(*) FROM artists")
    if cur.fetchone()[0] == 0:
        for a in ["Trio Lumina","DJ Faro","Compagnia Nova"]:
            cur.execute("INSERT INTO artists (name) VALUES (?)", (a,))
    cur.execute("SELECT COUNT(*) FROM formats")
    if cur.fetchone()[0] == 0:
        for f in ["Concerto","Spettacolo Teatrale","DJ Set"]:
            cur.execute("INSERT INTO formats (name) VALUES (?)", (f,))
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
            cur.execute("INSERT INTO people (name, role) VALUES (?,?)", (name, role))
    cur.execute("SELECT COUNT(*) FROM events")
    if cur.fetchone()[0] == 0:
        today = date.today()
        events = [
            ("Apertura Stagione", today.isoformat(), 1, 1, "Evento inaugurale"),
            ("Festa DJ Faro", (today + timedelta(days=3)).isoformat(), 3, 1, "DJ set all'aperto"),
            ("Compagnia Nova - prova", (today + timedelta(days=7)).isoformat(), 2, 1, "Prova generale"),
        ]
        for title, d, fmt, promoter, notes in events:
            cur.execute("INSERT INTO events (title,date,format_id,promoter_id,notes) VALUES (?,?,?,?,?)",
                        (title, d, fmt, promoter, notes))
        cur.execute("SELECT id FROM events")
        event_ids = [r[0] for r in cur.fetchall()]
        cur.execute("INSERT OR IGNORE INTO event_artists (event_id, artist_id) VALUES (?,?)", (event_ids[0], 1))
        cur.execute("INSERT OR IGNORE INTO event_artists (event_id, artist_id) VALUES (?,?)", (event_ids[1], 2))
        cur.execute("INSERT OR IGNORE INTO event_artists (event_id, artist_id) VALUES (?,?)", (event_ids[2], 3))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed()
