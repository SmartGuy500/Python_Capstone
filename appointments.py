from contextlib import closing
import sqlite3 

DB_FILE = "appointments.db"


class AppointmentDatabaseError(RuntimeError):
    """Raised when an appointment database operation fails."""


def create_table():
    try:
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
    except sqlite3.Error as error:
        raise AppointmentDatabaseError(
            f"Could not initialize the appointment database: {error}"
        ) from error


def add_appointments(patient_name, patient_contact, doctor, day, time, reason):
    try:
        with closing(sqlite3.connect(DB_FILE)) as connection, connection:
            connection.execute(
                "INSERT INTO appointments "
                "(patient_name, patient_contact, doctor, day, time, reason) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (patient_name, patient_contact, doctor, day, time, reason),
            )
    except sqlite3.Error as error:
        raise AppointmentDatabaseError(
            f"Could not add the appointment: {error}"
        ) from error


def get_appointments():
    try:
        with closing(sqlite3.connect(DB_FILE)) as connection, connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute("""
                SELECT id, patient_name, patient_contact, doctor, day, time, reason, status
                FROM appointments
                ORDER BY id
            """).fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as error:
        raise AppointmentDatabaseError(
            f"Could not retrieve appointments: {error}"
        ) from error


def update_appointments(id, patient_name, patient_contact, doctor, day, time, reason):
    try:
        with closing(sqlite3.connect(DB_FILE)) as connection, connection:
            connection.execute(
                "UPDATE appointments "
                "SET patient_name=?, patient_contact=?, doctor=?, day=?, time=?, reason=? "
                "WHERE id=?",
                (patient_name, patient_contact, doctor, day, time, reason, id),
            )
    except sqlite3.Error as error:
        raise AppointmentDatabaseError(
            f"Could not update appointment #{id}: {error}"
        ) from error


def delete_appointments(id):
    try:
        with closing(sqlite3.connect(DB_FILE)) as connection, connection:
            connection.execute("DELETE FROM appointments WHERE id=?", (id,))
    except sqlite3.Error as error:
        raise AppointmentDatabaseError(
            f"Could not delete appointment #{id}: {error}"
        ) from error


