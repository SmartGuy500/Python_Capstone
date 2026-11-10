import sqlite3 

print("Ready to start")

connection = sqlite3.connect("appointments.db")

cursor = connection.cursor()

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

cursor.execute("""
INSERT INTO appointments (patient_name, patient_contact, doctor, day, time, reason) VALUES (?,?,?,?,?,?)
""")

connection.commit()

connection.close()

print("Completed")

