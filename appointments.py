from contextlib import closing
import sqlite3 

DB_FILE = "appointments.db"


def create_table():
    with closing(sqlite3.connect(DB_FILE)) as connection, connection:
        connection.execute("""
        CREATE TABLE IF NOT EXISTS appointments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            patient_contact TEXT,
            doctor TEXT NOT NULL,
            day TEXT NOT NULL,
            time TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT "Booked"
        )
        """)


def add_appointments(patient_name, patient_contact, doctor, day, time, reason):
    with closing(sqlite3.connect(DB_FILE)) as connection, connection:
        connection.execute(
            "INSERT INTO appointments "
            "(patient_name, patient_contact, doctor, day, time, reason) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (patient_name, patient_contact, doctor, day, time, reason),
        )


def get_appointments():
    with closing(sqlite3.connect(DB_FILE)) as connection, connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute("""
            SELECT id, patient_name, patient_contact, doctor, day, time, reason, status
            FROM appointments
            ORDER BY id
        """).fetchall()
        return [dict(row) for row in rows]


def update_appointments(id, patient_name, patient_contact, doctor, day, time, reason):
    with closing(sqlite3.connect(DB_FILE)) as connection, connection:
        connection.execute(
            "UPDATE appointments "
            "SET patient_name=?, patient_contact=?, doctor=?, day=?, time=?, reason=? "
            "WHERE id=?",
            (patient_name, patient_contact, doctor, day, time, reason, id),
        )


def delete_appointments(id):
    with closing(sqlite3.connect(DB_FILE)) as connection, connection:
        connection.execute("DELETE FROM appointments WHERE id=?", (id,))


