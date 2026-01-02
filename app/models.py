from .db import get_conn
import pandas as pd

def fetch_artists():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM artists ORDER BY name", conn)
    conn.close()
    return df

def fetch_formats():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM formats ORDER BY name", conn)
    conn.close()
    return df

def fetch_people():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM people ORDER BY name", conn)
    conn.close()
    return df

def fetch_events(start_date=None, end_date=None):
    conn = get_conn()
    q = "SELECT e.*, f.name as format_name, p.name as promoter_name FROM events e LEFT JOIN formats f ON e.format_id=f.id LEFT JOIN people p ON e.promoter_id=p.id WHERE 1=1"
    params = []
    if start_date:
        q += " AND date(e.date) >= date(?)"
        params.append(start_date)
    if end_date:
        q += " AND date(e.date) <= date(?)"
        params.append(end_date)
    q += " ORDER BY date(e.date) ASC"
    df = pd.read_sql_query(q, conn, params=params)
    if not df.empty:
        df['artists'] = df['id'].apply(lambda eid: get_artists_for_event(eid))
    conn.close()
    return df

def get_artists_for_event(event_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT artist_id FROM event_artists WHERE event_id=?", (event_id,))
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]

def create_event(title, date_iso, format_id, promoter_id, notes, artist_ids):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO events (title,date,format_id,promoter_id,notes) VALUES (?,?,?,?,?)",
                (title, date_iso, format_id, promoter_id, notes))
    eid = cur.lastrowid
    for aid in artist_ids:
        cur.execute("INSERT INTO event_artists (event_id, artist_id) VALUES (?,?)", (eid, aid))
    conn.commit()
    conn.close()

def update_event(eid, title, date_iso, format_id, promoter_id, notes, artist_ids):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE events SET title=?, date=?, format_id=?, promoter_id=?, notes=? WHERE id=?",
                (title, date_iso, format_id, promoter_id, notes, eid))
    cur.execute("DELETE FROM event_artists WHERE event_id=", (eid,))
    for aid in artist_ids:
        cur.execute("INSERT INTO event_artists (event_id, artist_id) VALUES (?,?)", (eid, aid))
    conn.commit()
    conn.close()

def delete_event(eid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM event_artists WHERE event_id=", (eid,))
    cur.execute("DELETE FROM event_people WHERE event_id=", (eid,))
    cur.execute("DELETE FROM events WHERE id=", (eid,))
    conn.commit()
    conn.close()
