import sqlite3 

DB_FILE = "appointments.db"

print("Ready to start")

connection = sqlite3.connect(DB_FILE)

cursor = connection.cursor()


def create_table(): 
    cursor.execute("""
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
    connection.commit()
    connection.close()


def add_appointments(patient_name, patient_contact, doctor, day, time, reason): 
    cursor.execute(
    "INSERT INTO appointments (patient_name, patient_contact, doctor, day, time, reason) VALUES (?, ?, ?, ?, ?, ?)", (patient_name, patient_contact, doctor, day, time, reason)
    )
    connection.commit()
    connection.close()

def get_appointments(patient_name, patient_contact, doctor, day, time, reason): 
    cursor.execute("""
    "SELECT patient_name, patient_contact, doctor, day, time, reason FROM appointments" 
    """)
    rows=cursor.fetchall()
    connection.close()

    patients=[]
    for row in rows:
        patients.append({
            "patient_name": row[0], 
            "patient_contact": row[1],
            "doctor": row[2],
            "day": row[3],
            "time": row[4],
            "reason": row[5]
        })
    return patients

def update_appointments(id, patient_name, patient_contact, doctor, day, time, reason):
    cursor.execute(
    "UPDATE appointments SET patient_name= ?, patient_contact= ?, doctor= ?, day= ?, time= ?, reason=? WHERE id= ? (?, ?, ?, ?, ?, ?)", (patient_name, patient_contact, doctor, day, time, reason, id)
    )
    connection.commit()
    connection.close()

def delete_appointments(id):
    cursor.execute(
    "DELETE FROM appointments WHERE id= ?", (id)
    )
    connection.commit()
    connection.close()



print("Completed")

