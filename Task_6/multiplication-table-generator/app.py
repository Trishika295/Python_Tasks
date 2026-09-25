from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Multiplication Table Generator API is running!"
    })


@app.route("/api/multiplication-table", methods=["POST"])
def generate_multiplication_table():

    data = request.get_json()

    # Check whether data was received
    if not data:
        return jsonify({
            "error": "No data received."
        }), 400

    number = data.get("number")
    limit = data.get("limit")

    # Check whether both inputs are provided
    if number is None or limit is None:
        return jsonify({
            "error": "Please provide both number and limit."
        }), 400

    # Convert inputs to integers
    try:
        number = int(number)
        limit = int(limit)
    except (ValueError, TypeError):
        return jsonify({
            "error": "Please enter valid integer values."
        }), 400

    # Check limit
    if limit <= 0:
        return jsonify({
            "error": "Limit must be greater than 0."
        }), 400

    table = []

    # Generate multiplication table using a for loop
    for i in range(1, limit + 1):

        table.append({
            "multiplier": i,
            "result": number * i
        })

    return jsonify({
        "number": number,
        "limit": limit,
        "table": table
    })


# Terminal testing function
def terminal_test():

    print("\n==========================================")
    print("      MULTIPLICATION TABLE GENERATOR")
    print("==========================================")

    try:
        number = int(input("\nEnter the number: "))
        limit = int(input("Enter the limit: "))
    except ValueError:
        print("\nError: Please enter valid integer values.")
        return

    if limit <= 0:
        print("\nError: Limit must be greater than 0.")
        return

    print(f"\nMultiplication Table of {number}")
    print("-" * 40)

    for i in range(1, limit + 1):

        result = number * i

        print(f"{number} × {i} = {result}")

    print("-" * 40)
    print("Table generated successfully!")


# Start the required mode
if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        terminal_test()

    else:
        app.run(debug=True, port=5000)