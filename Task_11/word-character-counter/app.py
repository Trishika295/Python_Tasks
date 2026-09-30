from flask import Flask, request, jsonify
from flask_cors import CORS
import argparse

from text_analyzer import analyze_text


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Word and Character Counter API is running successfully."
    })


@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({
                "success": False,
                "message": "Please provide text."
            }), 400

        text = data["text"]

        if not isinstance(text, str):
            return jsonify({
                "success": False,
                "message": "Text must be a string."
            }), 400

        if not text.strip():
            return jsonify({
                "success": False,
                "message": "Please enter some text."
            }), 400

        statistics = analyze_text(text)

        return jsonify({
            "success": True,
            "statistics": statistics
        })

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


def run_terminal():
    print("\n" + "=" * 50)
    print("           WORD AND CHARACTER COUNTER")
    print("=" * 50)

    print("\nEnter your paragraph below.")
    print("Press ENTER on an empty line when finished.\n")

    lines = []

    while True:
        try:
            line = input()

            if line == "":
                break

            lines.append(line)

        except EOFError:
            break

    text = "\n".join(lines)

    if not text.strip():
        print("\nNo text entered.")
        print("Please enter a paragraph and try again.")
        return

    statistics = analyze_text(text)

    print("\n" + "=" * 50)
    print("                TEXT STATISTICS")
    print("=" * 50)

    print(f"Characters : {statistics['characters']}")
    print(f"Words      : {statistics['words']}")
    print(f"Sentences  : {statistics['sentences']}")
    print(f"Spaces     : {statistics['spaces']}")

    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Word and Character Counter"
    )

    parser.add_argument(
        "--terminal",
        action="store_true",
        help="Run the application in terminal mode"
    )

    args = parser.parse_args()

    if args.terminal:
        run_terminal()
    else:
        print("\n" + "=" * 50)
        print("       WORD AND CHARACTER COUNTER")
        print("=" * 50)
        print("Flask backend running at:")
        print("http://127.0.0.1:5000")
        print("=" * 50 + "\n")

        app.run(
            host="127.0.0.1",
            port=5000,
            debug=True
        )


if __name__ == "__main__":
    main()