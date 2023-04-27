import sqlite3
import datetime

days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

DB_NAME = "students.db"

def create_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        surname TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        email TEXT NOT NULL,
                        days TEXT NOT NULL,
                        time TEXT NOT NULL,
                        start_date TEXT NOT NULL,
                        end_date TEXT NOT NULL
                      )""")

    conn.commit()
    conn.close()


def fetch_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return students

def save_to_db(name, surname, phone, email, days, time, start_date, end_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, surname, phone, email, days, time, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name, surname, phone, email, ",".join(days), time, start_date, end_date))
    conn.commit()
    conn.close()

def check_availability(time, selected_days):
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()
    cursor.execute("SELECT days, time FROM students")
    students = cursor.fetchall()
    connection.close()

    day_counts = {day: 0 for day in days}
    max_students = 25

    for student in students:
        student_days = student[0].split(",")
        student_time = student[1]

        if student_time == time:
            for day in student_days:
                day_counts[day] += 1

    available_days = [day for day in selected_days if day_counts[day] < max_students]

    if set(available_days) == set(selected_days):
        return True, available_days
    else:
        return False, available_days

def delete_student(student_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()

def fetch_active_students():
    today = datetime.date.today()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE start_date <= ? AND end_date >= ?", (today, today))
    students = cursor.fetchall()
    conn.close()
    return students

def fetch_expired_students():
    today = datetime.date.today()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE end_date < ?", (today,))
    students = cursor.fetchall()
    conn.close()
    return students

def fetch_expired_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    current_date = datetime.date.today()
    cursor.execute("SELECT * FROM students WHERE end_date < ?", (current_date,))
    expired_students = cursor.fetchall()
    conn.close()
    return expired_students
