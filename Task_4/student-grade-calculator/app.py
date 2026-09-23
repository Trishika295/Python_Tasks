from flask import Flask, request, jsonify
from flask_cors import CORS

from grade_calculator import calculate_result

app = Flask(__name__)

CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Student Grade Calculator API is running."
    })


@app.route("/api/calculate", methods=["POST"])
def calculate():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400

        student_name = data.get(
            "student_name",
            ""
        ).strip()

        marks = data.get("marks")


        if not student_name:
            return jsonify({
                "success": False,
                "message": "Please enter the student's name."
            }), 400


        if not marks or not isinstance(marks, dict):
            return jsonify({
                "success": False,
                "message": "Subject marks are required."
            }), 400


        # Calculate result
        result = calculate_result(marks)


        return jsonify({
            "success": True,
            "student_name": student_name,
            "subjects": marks,
            "result": result
        }), 200


    except ValueError as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 400


    except Exception as error:

        print("Server Error:", error)

        return jsonify({
            "success": False,
            "message": "An unexpected server error occurred."
        }), 500


if __name__ == "__main__":

    print()
    print("=" * 50)
    print(" Student Grade Calculator Backend")
    print("=" * 50)
    print(" Server: http://127.0.0.1:5000")
    print(" API:    http://127.0.0.1:5000/api/calculate")
    print("=" * 50)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )