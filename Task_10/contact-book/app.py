from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import sys

app = Flask(__name__)
CORS(app)

# --------------------------------------------------
# File configuration
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "contacts.json")


# --------------------------------------------------
# Dictionary
# --------------------------------------------------

def load_contacts():
    """Load contacts from JSON file."""

    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, dict):
                return data

            return {}

    except (json.JSONDecodeError, OSError):
        return {}


contacts = load_contacts()


def save_contacts():
    """Save dictionary data to JSON file."""

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)


# --------------------------------------------------
# Validation
# --------------------------------------------------

def validate_contact(name, phone, email):
    """Validate contact information."""

    if not name or not phone or not email:
        return "All fields are required."

    if len(phone) < 7 or len(phone) > 15:
        return "Phone number must contain 7 to 15 digits."

    if not phone.isdigit():
        return "Phone number must contain only digits."

    if "@" not in email or "." not in email:
        return "Please enter a valid email address."

    return None


# ==================================================
# FLASK WEB API
# ==================================================

@app.route("/")
def home():
    return jsonify({
        "message": "Contact Book API is running successfully.",
        "project": "Contact Book Using Dictionaries",
        "status": "success"
    })


# --------------------------------------------------
# GET ALL CONTACTS
# --------------------------------------------------

@app.route("/api/contacts", methods=["GET"])
def get_contacts():

    return jsonify(contacts)


# --------------------------------------------------
# SEARCH CONTACTS
# --------------------------------------------------

@app.route("/api/contacts/search", methods=["GET"])
def search_contacts():

    query = request.args.get("q", "").strip().lower()

    if not query:
        return jsonify(contacts)

    results = {}

    for contact_id, contact in contacts.items():

        if (
            query in contact_id.lower()
            or query in contact["name"].lower()
            or query in contact["phone"].lower()
            or query in contact["email"].lower()
        ):
            results[contact_id] = contact

    return jsonify(results)


# --------------------------------------------------
# ADD CONTACT
# --------------------------------------------------

@app.route("/api/contacts", methods=["POST"])
def add_contact():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No contact data received."
        }), 400

    contact_id = data.get("id", "").strip()
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()

    # Validate ID
    if not contact_id:
        return jsonify({
            "error": "Contact ID is required."
        }), 400

    # Validate contact information
    validation_error = validate_contact(
        name,
        phone,
        email
    )

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    # Duplicate ID
    if contact_id in contacts:

        return jsonify({
            "error": "Contact ID already exists."
        }), 409

    # Duplicate phone
    for contact in contacts.values():

        if contact["phone"] == phone:

            return jsonify({
                "error": "Phone number already exists."
            }), 409

    # Dictionary key-value pair
    contacts[contact_id] = {
        "name": name,
        "phone": phone,
        "email": email
    }

    save_contacts()

    return jsonify({
        "message": "Contact added successfully.",
        "contact": contacts[contact_id]
    }), 201


# --------------------------------------------------
# UPDATE CONTACT
# --------------------------------------------------

@app.route("/api/contacts/<contact_id>", methods=["PUT"])
def update_contact(contact_id):

    if contact_id not in contacts:

        return jsonify({
            "error": "Contact not found."
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received."
        }), 400

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()

    validation_error = validate_contact(
        name,
        phone,
        email
    )

    if validation_error:

        return jsonify({
            "error": validation_error
        }), 400

    # Check duplicate phone number
    for cid, contact in contacts.items():

        if cid != contact_id and contact["phone"] == phone:

            return jsonify({
                "error": "Phone number already exists."
            }), 409

    contacts[contact_id] = {
        "name": name,
        "phone": phone,
        "email": email
    }

    save_contacts()

    return jsonify({
        "message": "Contact updated successfully.",
        "contact": contacts[contact_id]
    })


# --------------------------------------------------
# DELETE CONTACT
# --------------------------------------------------

@app.route("/api/contacts/<contact_id>", methods=["DELETE"])
def delete_contact(contact_id):

    if contact_id not in contacts:

        return jsonify({
            "error": "Contact not found."
        }), 404

    deleted_contact = contacts.pop(contact_id)

    save_contacts()

    return jsonify({
        "message": "Contact deleted successfully.",
        "contact": deleted_contact
    })


# ==================================================
# TERMINAL / CMD APPLICATION
# ==================================================

def print_line():
    print("-" * 65)


def display_contacts(contact_data=None):

    if contact_data is None:
        contact_data = contacts

    print()

    if not contact_data:

        print("No contacts available.")
        return

    print_line()

    print(
        f"{'ID':<10}"
        f"{'NAME':<22}"
        f"{'PHONE':<16}"
        f"{'EMAIL'}"
    )

    print_line()

    for contact_id, contact in contact_data.items():

        print(
            f"{contact_id:<10}"
            f"{contact['name']:<22}"
            f"{contact['phone']:<16}"
            f"{contact['email']}"
        )

    print_line()


def add_contact_terminal():

    print()
    print("ADD NEW CONTACT")
    print_line()

    contact_id = input("Enter Contact ID: ").strip()

    if not contact_id:

        print("Contact ID cannot be empty.")
        return

    if contact_id in contacts:

        print("Contact ID already exists.")
        return

    name = input("Enter Name: ").strip()
    phone = input("Enter Phone: ").strip()
    email = input("Enter Email: ").strip()

    validation_error = validate_contact(
        name,
        phone,
        email
    )

    if validation_error:

        print(validation_error)
        return

    # Duplicate phone
    for contact in contacts.values():

        if contact["phone"] == phone:

            print("Phone number already exists.")
            return

    contacts[contact_id] = {
        "name": name,
        "phone": phone,
        "email": email
    }

    save_contacts()

    print()
    print("Contact added successfully!")


def search_contact_terminal():

    print()
    print("SEARCH CONTACT")
    print_line()

    query = input(
        "Enter ID, name, phone or email: "
    ).strip().lower()

    if not query:

        print("Search query cannot be empty.")
        return

    results = {}

    for contact_id, contact in contacts.items():

        if (
            query in contact_id.lower()
            or query in contact["name"].lower()
            or query in contact["phone"].lower()
            or query in contact["email"].lower()
        ):

            results[contact_id] = contact

    print()

    if results:

        display_contacts(results)

    else:

        print("No matching contacts found.")


def update_contact_terminal():

    print()
    print("UPDATE CONTACT")
    print_line()

    contact_id = input(
        "Enter Contact ID to update: "
    ).strip()

    if contact_id not in contacts:

        print("Contact not found.")
        return

    current = contacts[contact_id]

    print()
    print("Press Enter to keep the current value.")

    name = input(
        f"Name [{current['name']}]: "
    ).strip()

    phone = input(
        f"Phone [{current['phone']}]: "
    ).strip()

    email = input(
        f"Email [{current['email']}]: "
    ).strip()

    if not name:
        name = current["name"]

    if not phone:
        phone = current["phone"]

    if not email:
        email = current["email"]

    validation_error = validate_contact(
        name,
        phone,
        email
    )

    if validation_error:

        print(validation_error)
        return

    # Check duplicate phone
    for cid, contact in contacts.items():

        if cid != contact_id and contact["phone"] == phone:

            print("Phone number already exists.")
            return

    contacts[contact_id] = {
        "name": name,
        "phone": phone,
        "email": email
    }

    save_contacts()

    print()
    print("Contact updated successfully!")


def delete_contact_terminal():

    print()
    print("DELETE CONTACT")
    print_line()

    contact_id = input(
        "Enter Contact ID to delete: "
    ).strip()

    if contact_id not in contacts:

        print("Contact not found.")
        return

    contact = contacts[contact_id]

    print()
    print(
        f"Name : {contact['name']}"
    )
    print(
        f"Phone: {contact['phone']}"
    )
    print(
        f"Email: {contact['email']}"
    )

    confirm = input(
        "\nAre you sure you want to delete? (y/n): "
    ).strip().lower()

    if confirm == "y":

        contacts.pop(contact_id)

        save_contacts()

        print("Contact deleted successfully!")

    else:

        print("Delete operation cancelled.")


def terminal_menu():

    while True:

        print()
        print("=" * 65)
        print("              CONTACT BOOK")
        print("       Python Dictionary Management")
        print("=" * 65)

        print()
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        print()

        choice = input(
            "Enter your choice (1-6): "
        ).strip()

        if choice == "1":

            add_contact_terminal()

        elif choice == "2":

            display_contacts()

        elif choice == "3":

            search_contact_terminal()

        elif choice == "4":

            update_contact_terminal()

        elif choice == "5":

            delete_contact_terminal()

        elif choice == "6":

            print()
            print("Thank you for using Contact Book!")
            print("Goodbye!")
            break

        else:

            print()
            print("Invalid choice. Please enter 1-6.")


# ==================================================
# APPLICATION START
# ==================================================

if __name__ == "__main__":

    # Terminal mode
    if len(sys.argv) > 1 and sys.argv[1].lower() in [
        "--terminal",
        "-t",
        "terminal",
        "cli"
    ]:

        terminal_menu()

    # Browser / Flask mode
    else:

        print()
        print("=" * 55)
        print("CONTACT BOOK - FLASK SERVER")
        print("=" * 55)
        print("Browser API: http://127.0.0.1:5000")
        print("Terminal mode: python app.py --terminal")
        print("=" * 55)
        print()

        app.run(
            host="127.0.0.1",
            port=5000,
            debug=True
        )