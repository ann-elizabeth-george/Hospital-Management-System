import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Database Configuration - Updated to match running MySQL80 service
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'hospital_db'
}

def get_connection():
    """Establishes and returns a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        print("\n[!] Could not connect to MySQL. Please check your credentials in DB_CONFIG.")
        return None

# --- PATIENT FUNCTIONS ---

def add_patient():
    print("\n--- Add New Patient ---")
    name = input("Enter Name: ")
    try:
        age = int(input("Enter Age: "))
    except ValueError:
        print("Invalid Age! Please enter a number.")
        return
    gender = input("Enter Gender: ")

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO patients (name, age, gender) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, age, gender))
        conn.commit()
        print(f"Patient '{name}' added successfully!")
        cursor.close()
        conn.close()

def view_patients():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        
        print("\n" + "="*50)
        print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Gender':<10}")
        print("-" * 50)
        for p in patients:
            print(f"{p[0]:<5} {p[1]:<20} {p[2]:<5} {p[3]:<10}")
        print("="*50)
        
        cursor.close()
        conn.close()

def delete_patient():
    view_patients()
    try:
        p_id = int(input("Enter Patient ID to delete: "))
    except ValueError:
        print("Invalid ID!")
        return

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE patient_id = %s", (p_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Patient ID {p_id} deleted.")
        else:
            print("Patient ID not found.")
        cursor.close()
        conn.close()

def update_patient():
    view_patients()
    try:
        p_id = int(input("Enter Patient ID to update: "))
    except ValueError:
        print("Invalid ID!")
        return
    
    name = input("Enter New Name (leave blank to keep current): ")
    age_input = input("Enter New Age (leave blank to keep current): ")
    gender = input("Enter New Gender (leave blank to keep current): ")

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        # Fetch current values if needed, or just build dynamic query
        # For simplicity, we'll ask for all or keep blank
        if name:
            cursor.execute("UPDATE patients SET name = %s WHERE patient_id = %s", (name, p_id))
        if age_input:
            cursor.execute("UPDATE patients SET age = %s WHERE patient_id = %s", (int(age_input), p_id))
        if gender:
            cursor.execute("UPDATE patients SET gender = %s WHERE patient_id = %s", (gender, p_id))
        
        conn.commit()
        print("Patient details updated!")
        cursor.close()
        conn.close()

# --- DOCTOR FUNCTIONS ---

def add_doctor():
    print("\n--- Add New Doctor ---")
    name = input("Enter Name: ")
    spec = input("Enter Specialization: ")

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO doctors (name, specialization) VALUES (%s, %s)"
        cursor.execute(query, (name, spec))
        conn.commit()
        print(f"Doctor '{name}' added successfully!")
        cursor.close()
        conn.close()

def view_doctors():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()
        
        print("\n" + "="*50)
        print(f"{'ID':<5} {'Name':<20} {'Specialization':<20}")
        print("-" * 50)
        for d in doctors:
            print(f"{d[0]:<5} {d[1]:<20} {d[2]:<20}")
        print("="*50)
        
        cursor.close()
        conn.close()

def delete_doctor():
    view_doctors()
    try:
        d_id = int(input("Enter Doctor ID to delete: "))
    except ValueError:
        print("Invalid ID!")
        return

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctors WHERE doctor_id = %s", (d_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Doctor ID {d_id} deleted.")
        else:
            print("Doctor ID not found.")
        cursor.close()
        conn.close()

# --- APPOINTMENT FUNCTIONS ---

def book_appointment():
    view_patients()
    try:
        p_id = int(input("Enter Patient ID: "))
    except ValueError:
        print("Invalid ID!")
        return

    view_doctors()
    try:
        d_id = int(input("Enter Doctor ID: "))
    except ValueError:
        print("Invalid ID!")
        return
    
    date_str = input("Enter Appointment Date (YYYY-MM-DD): ")
    try:
        # Validate date format
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format! Use YYYY-MM-DD.")
        return

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO appointments (patient_id, doctor_id, appointment_date) VALUES (%s, %s, %s)"
        cursor.execute(query, (p_id, d_id, date_str))
        conn.commit()
        print("Appointment booked successfully!")
        cursor.close()
        conn.close()

def view_appointments():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        # SQL JOIN to display names instead of just IDs
        query = """
            SELECT a.appointment_id, p.name, d.name, a.appointment_date
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
        """
        cursor.execute(query)
        apps = cursor.fetchall()
        
        print("\n" + "="*70)
        print(f"{'ID':<5} {'Patient Name':<20} {'Doctor Name':<20} {'Date':<15}")
        print("-" * 70)
        for a in apps:
            print(f"{a[0]:<5} {a[1]:<20} {a[2]:<20} {str(a[3]):<15}")
        print("="*70)
        
        cursor.close()
        conn.close()

# --- MAIN MENU ---

def main_menu():
    while True:
        print("\n--- HOSPITAL MANAGEMENT SYSTEM ---")
        print("1. Add Patient")
        print("2. Add Doctor")
        print("3. Book Appointment")
        print("4. View All Patients")
        print("5. View All Doctors")
        print("6. View Appointments")
        print("7. Delete Patient")
        print("8. Delete Doctor")
        print("9. Update Patient (Extra)")
        print("10. Exit")
        
        choice = input("\nEnter choice (1-10): ")
        
        if choice == '1':
            add_patient()
        elif choice == '2':
            add_doctor()
        elif choice == '3':
            book_appointment()
        elif choice == '4':
            view_patients()
        elif choice == '5':
            view_doctors()
        elif choice == '6':
            view_appointments()
        elif choice == '7':
            delete_patient()
        elif choice == '8':
            delete_doctor()
        elif choice == '9':
            update_patient()
        elif choice == '10':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
