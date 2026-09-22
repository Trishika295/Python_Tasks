from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow React frontend to communicate with Flask
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Even & Odd Number Checker API is running"
    })


@app.route("/api/check-number", methods=["POST"])
def check_number():

    data = request.get_json(silent=True)

    if not data or "number" not in data:
        return jsonify({
            "success": False,
            "message": "Please enter a number."
        }), 400

    try:
        number = int(data["number"])
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "message": "Please enter a valid integer."
        }), 400

    # Even / Odd logic
    if number % 2 == 0:
        result = "Even"
    else:
        result = "Odd"

    return jsonify({
        "success": True,
        "number": number,
        "result": result,
        "message": f"{number} is an {result.lower()} number."
    })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )