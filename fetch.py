import os
import random
import json
from flask import Flask, session, request, jsonify, send_from_directory
from flask_session import Session

app = Flask(__name__, static_folder=".", static_url_path="")
app.secret_key = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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

        # If JSON is { "WORDS": [ ... ] }, use data["WORDS"]
        if isinstance(data, dict) and "WORDS" in data and isinstance(data["WORDS"], list):
            raw_list = data["WORDS"]
        # If JSON is already a flat array ([ "apple", "bench", ... ]), use it directly
        elif isinstance(data, list):
            raw_list = data
        else:
            print("Error: words.json must be either a flat array or an object with key \"WORDS\".")
            all_words = []
            return

        # Keep only strings that are exactly 5 letters (alphabetic)
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

# Load immediately when the module is imported/run
fetch_word_list()
