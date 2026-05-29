from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "hospital_secret_key"

# Database Configuration (MySQL80 Defaults)
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'hospital_db'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    stats = {'patients': 0, 'doctors': 0, 'appointments': 0}
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as count FROM patients")
        stats['patients'] = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) as count FROM doctors")
        stats['doctors'] = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) as count FROM appointments")
        stats['appointments'] = cursor.fetchone()['count']
        cursor.close()
        conn.close()
    return render_template('index.html', stats=stats)

# --- PATIENTS ---
@app.route('/patients', methods=['GET', 'POST'])
def patients():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO patients (name, age, gender) VALUES (%s, %s, %s)", (name, age, gender))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Patient added successfully!", "success")
            return redirect(url_for('patients'))
    
    patient_list = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients")
        patient_list = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('patients.html', patients=patient_list)

@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE patient_id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Patient deleted!", "danger")
    return redirect(url_for('patients'))

# --- DOCTORS ---
@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO doctors (name, specialization) VALUES (%s, %s)", (name, specialization))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Doctor added successfully!", "success")
            return redirect(url_for('doctors'))
    
    doctor_list = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM doctors")
        doctor_list = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('doctors.html', doctors=doctor_list)

@app.route('/delete_doctor/<int:id>')
def delete_doctor(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctors WHERE doctor_id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Doctor deleted!", "danger")
    return redirect(url_for('doctors'))

# --- APPOINTMENTS ---
@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    conn = get_db_connection()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO appointments (patient_id, doctor_id, appointment_date) VALUES (%s, %s, %s)", (patient_id, doctor_id, date))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Appointment booked!", "success")
            return redirect(url_for('appointments'))
    
    appointment_list = []
    patients_list = []
    doctors_list = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        # JOIN for names
        query = """
            SELECT a.appointment_id, p.name as p_name, d.name as d_name, a.appointment_date 
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
        """
        cursor.execute(query)
        appointment_list = cursor.fetchall()
        
        cursor.execute("SELECT * FROM patients")
        patients_list = cursor.fetchall()
        cursor.execute("SELECT * FROM doctors")
        doctors_list = cursor.fetchall()
        
        cursor.close()
        conn.close()
    return render_template('appointments.html', appointments=appointment_list, patients=patients_list, doctors=doctors_list)

@app.route('/delete_appointment/<int:id>')
def delete_appointment(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM appointments WHERE appointment_id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Appointment cancelled!", "danger")
    return redirect(url_for('appointments'))

if __name__ == '__main__':
    app.run(debug=True)
