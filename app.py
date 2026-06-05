from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "port": 3307,
    "user": "root",
    "password": "Vishumaanu#0508",   # yahan apna working password rakho
    "database": "student_placement_db"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def predict_placement(student):
    cgpa = float(student.get("cgpa", 0) or 0)
    internships = int(student.get("internship_count", 0) or 0)
    projects = int(student.get("project_count", 0) or 0)

    python_skill = int(student.get("python_skill", 0) or 0)
    sql_skill = int(student.get("sql_skill", 0) or 0)
    communication_skill = int(student.get("communication_skill", 0) or 0)
    aptitude_score = int(student.get("aptitude_score", 0) or 0)

    placed = str(student.get("placement_status", "")).strip().lower() == "placed"

    # Normalized score out of 100
    score = (
        (cgpa / 10) * 30 +
        (aptitude_score / 100) * 25 +
        (python_skill / 10) * 10 +
        (sql_skill / 10) * 10 +
        (communication_skill / 10) * 10 +
        min(internships, 3) * 5 +
        min(projects, 5) * 2
    )

    if score >= 75:
        chance = "high"
    elif score >= 50:
        chance = "medium"
    else:
        chance = "low"

    labels = {
        "high": "High chances to get placed",
        "medium": "Medium chances to get placed",
        "low": "Low chances to get placed"
    }

    return {
        "chance": chance,
        "placed": placed,
        "label": labels[chance],
        "score": round(score, 1)
    }

def fetch_students(where_clause="", params=()):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    sql = f"SELECT * FROM students {where_clause}"
    cur.execute(sql, params)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    for r in rows:
        r["prediction"] = predict_placement(r)

        # template compatibility
        r["internships"] = r.get("internship_count", 0)
        r["projects"] = r.get("project_count", 0)
        r["skills_count"] = (
            int(r.get("python_skill", 0) or 0) +
            int(r.get("sql_skill", 0) or 0) +
            int(r.get("communication_skill", 0) or 0)
        )
        r["placed"] = str(r.get("placement_status", "")).strip().lower() == "placed"

    return rows

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/student/<student_id>")
def student_report(student_id):
    try:
        rows = fetch_students("WHERE student_id = %s", (student_id,))
        if not rows:
            return render_template(
                "filter.html",
                students=[],
                title=f"Student {student_id} Not Found"
            )
        return render_template(
            "filter.html",
            students=rows,
            title=f"Report for Student ID: {student_id}"
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/report/student", methods=["POST"])
def single_report():
    try:
        sid = request.form.get("student_id", "").strip()

        if not sid:
            return jsonify({"error": "No student ID provided"}), 400

        rows = fetch_students("WHERE student_id = %s", (sid,))

        if not rows:
            return jsonify({"error": f"Student {sid} not found"}), 404

        student = rows[0]
        return jsonify(student)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/report/all")
def all_report():
    try:
        students = fetch_students()
        return render_template(
            "filter.html",
            students=students,
            title="All Students – Placement Prediction"
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/report/high")
def high_report():
    try:
        students = [s for s in fetch_students() if s["prediction"]["chance"] == "high"]
        return render_template(
            "filter.html",
            students=students,
            title="Students with High Placement Chances"
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/report/medium")
def medium_report():
    try:
        students = [s for s in fetch_students() if s["prediction"]["chance"] == "medium"]
        return render_template(
            "filter.html",
            students=students,
            title="Students with Medium Placement Chances"
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/report/low")
def low_report():
    try:
        students = [s for s in fetch_students() if s["prediction"]["chance"] == "low"]
        return render_template(
            "filter.html",
            students=students,
            title="Students with Low Placement Chances"
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)