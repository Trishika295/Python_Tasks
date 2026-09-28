from flask import Flask, request, jsonify
from flask_cors import CORS

from student_manager import StudentManager


app = Flask(__name__)

CORS(app)

manager = StudentManager()


# ==========================================
# GET ALL STUDENTS
# ==========================================

@app.route("/api/students", methods=["GET"])
def get_students():

    return jsonify(
        manager.get_students()
    )


# ==========================================
# ADD STUDENT
# ==========================================

@app.route("/api/students", methods=["POST"])
def add_student():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "No data provided."
        }), 400

    name = data.get("name")
    marks = data.get("marks")

    try:

        student = manager.add_student(
            name,
            marks
        )

        return jsonify({
            "message": "Student added successfully.",
            "student": student
        }), 201

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400


# ==========================================
# SEARCH STUDENTS
# ==========================================

@app.route("/api/students/search", methods=["GET"])
def search_students():

    name = request.args.get(
        "name",
        ""
    )

    results = manager.search_students(
        name
    )

    return jsonify(results)


# ==========================================
# SORT STUDENTS
# ==========================================

@app.route("/api/students/sort", methods=["GET"])
def sort_students():

    order = request.args.get(
        "order",
        "desc"
    )

    if order not in ["asc", "desc"]:

        return jsonify({
            "error":
            "Order must be 'asc' or 'desc'."
        }), 400

    students = manager.sort_students(
        order
    )

    return jsonify(students)


# ==========================================
# STATISTICS
# ==========================================

@app.route(
    "/api/students/statistics",
    methods=["GET"]
)
def statistics():

    return jsonify(
        manager.get_statistics()
    )


# ==========================================
# DELETE STUDENT
# ==========================================

@app.route(
    "/api/students/<int:student_id>",
    methods=["DELETE"]
)
def delete_student(student_id):

    deleted = manager.delete_student(
        student_id
    )

    if not deleted:

        return jsonify({
            "error": "Student not found."
        }), 404

    return jsonify({
        "message":
        "Student deleted successfully."
    })


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "success",
        "message":
        "Student Records API is running."
    })


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    import sys

    # --------------------------------------
    # Run CLI
    # --------------------------------------

    if "--cli" in sys.argv:

        from student_manager import run_cli

        run_cli()

    # --------------------------------------
    # Run Browser / Flask
    # --------------------------------------

    else:

        print("\n" + "=" * 60)

        print(
            "STUDENT RECORDS MANAGEMENT SYSTEM"
        )

        print("=" * 60)

        print(
            "\nFlask backend is running at:"
        )

        print(
            "http://127.0.0.1:5000"
        )

        print(
            "\nReact frontend should run at:"
        )

        print(
            "http://localhost:5173"
        )

        print(
            "\nTo run the CMD version:"
        )

        print(
            "python app.py --cli"
        )

        print("=" * 60 + "\n")

        app.run(
            host="127.0.0.1",
            port=5000,
            debug=True
        )