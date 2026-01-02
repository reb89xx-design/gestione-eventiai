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
    try:
        df = pd.read_sql_query(q, conn, params=params)
    except Exception:
        conn.close()
        return pd.DataFrame()
    if df is None or df.empty:
        conn.close()
        return pd.DataFrame()
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
    cur.execute("DELETE FROM event_artists WHERE event_id=?", (eid,))
    for aid in artist_ids:
        cur.execute("INSERT INTO event_artists (event_id, artist_id) VALUES (?,?)", (eid, aid))
    conn.commit()
    conn.close()

def delete_event(eid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM event_artists WHERE event_id=?", (eid,))
    cur.execute("DELETE FROM event_people WHERE event_id=?", (eid,))
    cur.execute("DELETE FROM events WHERE id=?", (eid,))
    conn.commit()
    conn.close()

# ---- CRUD helpers for structure management ----

def create_artist(name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO artists (name) VALUES (?)", (name,))
    conn.commit()
    aid = cur.lastrowid
    conn.close()
    return aid

def update_artist(aid, name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE artists SET name=? WHERE id=?", (name, aid))
    conn.commit()
    conn.close()

def delete_artist(aid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM event_artists WHERE artist_id=?", (aid,))
    cur.execute("DELETE FROM artists WHERE id=?", (aid,))
    conn.commit()
    conn.close()

def create_format(name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO formats (name) VALUES (?)", (name,))
    conn.commit()
    fid = cur.lastrowid
    conn.close()
    return fid

def update_format(fid, name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE formats SET name=? WHERE id=?", (name, fid))
    conn.commit()
    conn.close()

def delete_format(fid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM events WHERE format_id=?", (fid,))
    cur.execute("DELETE FROM formats WHERE id=?", (fid,))
    conn.commit()
    conn.close()

def create_person(name, role):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO people (name, role) VALUES (?,?)", (name, role))
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid

def update_person(pid, name, role):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE people SET name=?, role=? WHERE id=?", (name, role, pid))
    conn.commit()
    conn.close()

def delete_person(pid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM event_people WHERE person_id=?", (pid,))
    cur.execute("DELETE FROM people WHERE id=?", (pid,))
    conn.commit()
    conn.close()