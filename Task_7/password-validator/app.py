from flask import Flask, request, jsonify
from flask_cors import CORS
import string
import sys


# ============================================================
# FLASK APPLICATION SETUP
# ============================================================

app = Flask(__name__)
CORS(app)

MIN_PASSWORD_LENGTH = 8


# ============================================================
# PASSWORD VALIDATION FUNCTION
# ============================================================

def validate_password(password):
    """
    Validate a password using the required rules.

    Requirements:
    1. Minimum 8 characters
    2. At least one uppercase letter
    3. At least one lowercase letter
    4. At least one number
    5. At least one special character
    """

    has_uppercase = False
    has_lowercase = False
    has_number = False
    has_special = False

    # Check each character in the password
    for character in password:

        if character in string.ascii_uppercase:
            has_uppercase = True

        elif character in string.ascii_lowercase:
            has_lowercase = True

        elif character in string.digits:
            has_number = True

        elif character in string.punctuation:
            has_special = True

    # Store validation messages
    messages = []

    # Check minimum length
    if len(password) < MIN_PASSWORD_LENGTH:
        messages.append(
            "Password must contain at least 8 characters."
        )

    # Check uppercase letter
    if not has_uppercase:
        messages.append(
            "Password must contain at least one uppercase letter."
        )

    # Check lowercase letter
    if not has_lowercase:
        messages.append(
            "Password must contain at least one lowercase letter."
        )

    # Check number
    if not has_number:
        messages.append(
            "Password must contain at least one number."
        )

    # Check special character
    if not has_special:
        messages.append(
            "Password must contain at least one special character."
        )

    # Password is valid if there are no error messages
    is_valid = len(messages) == 0

    return {
        "valid": is_valid,

        "requirements": {
            "minimum_length": len(password) >= MIN_PASSWORD_LENGTH,
            "uppercase": has_uppercase,
            "lowercase": has_lowercase,
            "number": has_number,
            "special_character": has_special
        },

        "messages": messages
    }


# ============================================================
# FLASK API ROUTE
# ============================================================

@app.route("/api/validate-password", methods=["POST"])
def validate_password_api():

    # Get JSON data from React
    data = request.get_json()

    # Check whether data was received
    if not data:

        return jsonify({
            "valid": False,
            "requirements": {},
            "messages": [
                "No data was received."
            ]
        }), 400

    # Check whether password exists
    if "password" not in data:

        return jsonify({
            "valid": False,
            "requirements": {},
            "messages": [
                "Password is required."
            ]
        }), 400

    password = data["password"]

    # Check password data type
    if not isinstance(password, str):

        return jsonify({
            "valid": False,
            "requirements": {},
            "messages": [
                "Password must be a string."
            ]
        }), 400

    # Validate password
    result = validate_password(password)

    # Return validation result to React
    return jsonify(result)


# ============================================================
# FLASK HEALTH CHECK
# ============================================================

@app.route("/api/health", methods=["GET"])
def health_check():

    return jsonify({
        "status": "Backend is running successfully"
    })


# ============================================================
# TERMINAL / CMD VERSION
# ============================================================

def run_terminal_validator():

    print()
    print("=" * 55)
    print("        SIMPLE PASSWORD VALIDATOR")
    print("=" * 55)

    print()

    print("Password Requirements:")
    print("1. Minimum 8 characters")
    print("2. At least one uppercase letter")
    print("3. At least one lowercase letter")
    print("4. At least one number")
    print("5. At least one special character")

    print()
    print("Enter your password below.")
    print()

    # Get password from the user
    password = input("Enter password: ")

    # Validate password
    result = validate_password(password)

    print()
    print("-" * 55)

    # Display result
    if result["valid"]:

        print("✓ PASSWORD IS VALID")
        print()
        print("All password requirements are satisfied.")

    else:

        print("✕ PASSWORD IS INVALID")
        print()
        print("Please fix the following:")

        for message in result["messages"]:

            print("•", message)

    print("-" * 55)
    print()


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    # Terminal mode
    if "--terminal" in sys.argv:

        run_terminal_validator()

    # Browser / Flask mode
    else:

        print()
        print("=" * 55)
        print("      SIMPLE PASSWORD VALIDATOR")
        print("=" * 55)

        print()
        print("Flask backend is running.")
        print()
        print("Backend URL:")
        print("http://127.0.0.1:5000")

        print()
        print("React frontend URL:")
        print("http://localhost:5173")

        print()
        print("API endpoint:")
        print("http://127.0.0.1:5000/api/validate-password")

        print()
        print("=" * 55)
        print()

        app.run(
            host="127.0.0.1",
            port=5000,
            debug=True
        )