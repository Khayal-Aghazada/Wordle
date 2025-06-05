# app.py
import os
import random
import json
from flask import Flask, session, request, jsonify, send_from_directory
from flask_session import Session

app = Flask(__name__, static_folder=".", static_url_path="")
app.secret_key = os.urandom(24)

# Use filesystem-based sessions so each user gets their own secret word
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# all_words will hold the full list of 5-letter words loaded from local words.json
all_words = []


def fetch_word_list():
    """
    Load five‐letter words from a local JSON file called 'words.json'.
    If the JSON is an object containing a top‐level key "WORDS",
    it will pull the array from data["WORDS"]. Otherwise, if the JSON
    is already a flat array, it will use that array directly.
    """
    global all_words
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "words.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Determine where the actual word list lives:
        if isinstance(data, dict) and "WORDS" in data and isinstance(data["WORDS"], list):
            raw_list = data["WORDS"]
        elif isinstance(data, list):
            raw_list = data
        else:
            print("Error: words.json must be either a flat array or an object with key \"WORDS\".")
            all_words = []
            return

        # Filter to ensure each entry is exactly 5 alphabetical characters
        filtered = []
        for w in raw_list:
            if isinstance(w, str):
                w_stripped = w.strip().lower()
                if len(w_stripped) == 5 and w_stripped.isalpha():
                    filtered.append(w_stripped)

        all_words = filtered
        if not all_words:
            print("Warning: words.json loaded but no valid 5‐letter entries found.")
        else:
            print(f"Loaded {len(all_words)} five‐letter words from words.json.")

    except FileNotFoundError:
        print("Error: 'words.json' not found in the same directory as app.py.")
        all_words = []
    except json.JSONDecodeError as e:
        print(f"Error parsing words.json: {e}")
        all_words = []
    except Exception as e:
        print(f"Unexpected error loading words.json: {e}")
        all_words = []


# Immediately load the word list from local file
fetch_word_list()


@app.route("/", methods=["GET"])
def serve_index():
    # Serve the frontend (index.html should be in the same folder as this app.py)
    return send_from_directory(".", "index.html")


@app.route("/api/new", methods=["GET"])
def new_game():
    """Start a new game by picking a random secret word and storing it in session."""
    if not all_words:
        return jsonify({"error": "Word list not loaded (words.json missing or invalid)"}), 500

    secret = random.choice(all_words)
    session["secret_word"] = secret
    session["attempts"] = 0
    return jsonify({"status": "ok"})


@app.route("/api/guess", methods=["POST"])
def guess():
    """
    Expect JSON: { "guess": "abcde" }
    Return JSON: {
        "feedback": ["correct"/"present"/"absent", ...],
        "status": "continue"/"win"/"lose",
        "answer": "xxxxx"  # only if lose
    }
    """
    data = request.get_json()
    if not data or "guess" not in data:
        return jsonify({"error": "Missing guess"}), 400

    guess = data["guess"].lower().strip()
    if len(guess) != 5 or not guess.isalpha():
        return jsonify({"error": "Guess must be exactly five letters"}), 400

    secret = session.get("secret_word")
    if not secret:
        return jsonify({"error": "No active game. Call /api/new first."}), 400

    # Increment attempt counter
    session["attempts"] = session.get("attempts", 0) + 1
    attempts = session["attempts"]

    # Build feedback array
    feedback = ["absent"] * 5
    secret_chars = list(secret)
    guess_chars = list(guess)

    # First pass: mark correct letters (green) and "consume" them
    for i in range(5):
        if guess_chars[i] == secret_chars[i]:
            feedback[i] = "correct"
            secret_chars[i] = None

    # Second pass: mark present (yellow) or absent (gray)
    for i in range(5):
        if feedback[i] == "correct":
            continue
        if guess_chars[i] in secret_chars:
            feedback[i] = "present"
            # Remove only the first matching occurrence
            secret_chars[secret_chars.index(guess_chars[i])] = None
        else:
            feedback[i] = "absent"

    # Determine game status
    if all(f == "correct" for f in feedback):
        return jsonify({"feedback": feedback, "status": "win"})

    if attempts >= 6:
        return jsonify(
            {
                "feedback": feedback,
                "status": "lose",
                "answer": secret,
            }
        )

    return jsonify({"feedback": feedback, "status": "continue"})


if __name__ == "__main__":
    # Run on port 5000 by default
    app.run(debug=True)
