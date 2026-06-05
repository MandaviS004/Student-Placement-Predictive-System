import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="maanuvishu#0508",
    database="student_placement_db",
    port=3307
)

cursor = conn.cursor()

student_id = int(input("Enter Student ID: "))

query = "SELECT * FROM students WHERE student_id = %s"
cursor.execute(query, (student_id,))

row = cursor.fetchone()

if row:
    print("\n----- STUDENT PLACEMENT REPORT -----")
    print(f"Student ID           : {row[0]}")
    print(f"Name                 : {row[1]}")
    print(f"Department           : {row[2]}")
    print(f"CGPA                 : {row[3]}")
    print(f"Attendance           : {row[4]}")
    print(f"Python Skill         : {row[5]}")
    print(f"SQL Skill            : {row[6]}")
    print(f"Communication Skill  : {row[7]}")
    print(f"Aptitude Score       : {row[8]}")
    print(f"Internship Count     : {row[9]}")
    print(f"Project Count        : {row[10]}")
    print(f"Certification Count  : {row[11]}")
    print(f"Placement Status     : {row[12]}")
else:
    print("Student not found.")

cursor.close()
conn.close()