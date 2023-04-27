from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

from datetime import datetime, timedelta

def calculate_total_sessions_and_fee(start_date, end_date, days, fees_per_day):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    total_sessions = 0
    total_fee = 0
    date = start_date
    while date <= end_date:
        day_name = date.strftime('%A')
        if day_name in days:
            total_sessions += 1
            total_fee += fees_per_day[day_name]
        date += timedelta(days=1)
    
    return total_sessions, total_fee

def create_database():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 student_name TEXT NOT NULL,
                 student_surname TEXT NOT NULL,
                 gender TEXT NOT NULL,
                 student_phone TEXT NOT NULL,
                 parent_name TEXT NOT NULL,
                 parent_surname TEXT NOT NULL,
                 parent_phone TEXT NOT NULL,
                 parent_email TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    

def add_student(student_name, student_surname, gender, student_phone, parent_name, parent_surname, parent_phone, parent_email):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (student_name, student_surname, gender, student_phone, parent_name, parent_surname, parent_phone, parent_email) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (student_name, student_surname, gender, student_phone, parent_name, parent_surname, parent_phone, parent_email))
    conn.commit()
    conn.close()

def create_services_table():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS services
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 student_id INTEGER NOT NULL,
                 table_number INTEGER NOT NULL,
                 days TEXT NOT NULL,
                 time_slot TEXT NOT NULL,
                 FOREIGN KEY (student_id) REFERENCES students (id))''')
    conn.commit()
    conn.close()

def add_service(student_id, table_number, days, time_slots):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    days_str = ','.join(days)
    time_slots_str = ','.join([f'{day}:{time_slot}' for day, time_slot in time_slots.items()])
    c.execute("INSERT INTO services (student_id, table_number, days, time_slot) VALUES (?, ?, ?, ?)",
              (student_id, table_number, days_str, time_slots_str))
    conn.commit()
    service_id = c.lastrowid
    conn.close()
    return service_id

def get_all_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return students

def create_sales_table():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sales
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 student_id INTEGER NOT NULL,
                 service_id INTEGER NOT NULL,
                 start_date TEXT NOT NULL,
                 end_date TEXT NOT NULL,
                 total_sessions INTEGER NOT NULL,
                 total_fee REAL NOT NULL,
                 FOREIGN KEY (student_id) REFERENCES students (id),
                 FOREIGN KEY (
                 FOREIGN KEY (service_id) REFERENCES services (id))''')
    conn.commit()
    conn.close()

def add_sale(student_id, service_id, start_date, end_date, total_sessions, total_fee):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("INSERT INTO sales (student_id, service_id, start_date, end_date, total_sessions, total_fee) VALUES (?, ?, ?, ?, ?, ?)",
              (student_id, service_id, start_date, end_date, total_sessions, total_fee))
    conn.commit()
    sale_id = c.lastrowid
    conn.close()
    return sale_id

def get_student_sales(student_id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sales WHERE student_id=?", (student_id,))
    sales = c.fetchall()
    conn.close()
    return sales

def get_student(student_id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = c.fetchone()
    conn.close()
    return student

create_services_table()
create_database()
create_sales_table()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mevcut yönlendiriciler ve işlevler burada devam ediyor
# (Önceki kodda olduğu gibi '/students_with_services' yönlendiricisi dahil)

if __name__ == '__main__':
    app.run(debug=True)
