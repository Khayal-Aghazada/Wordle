🎮 **Mini Wordle Web App**
A lightweight Wordle-style game built with Flask (Python) on the backend and a single-page HTML/CSS/JavaScript frontend. Guess a random 5-letter word in six tries!

---

🌟 **Features**

✅ **User Side**

* 🎲 Start a new game with a random 5-letter secret word from your own `words.json`
* 🎯 Enter guesses via on-screen keyboard or physical keyboard
* 🟩 Letters turn **green** if correct (right letter, right spot)
* 🟨 Letters turn **yellow** if present (right letter, wrong spot)
* ⬜ Letters turn **gray** if absent (not in the word)
* ✏️ “EN” key to submit, “BS” key to delete (shortened labels for clarity)
* 📣 Win message (“🎉 You guessed it!”) or lose message with answer reveal (“💔 Game over. Word was “\_\_\_\_\_””)
* 🔄 Six attempts—six rows of five tiles

---

🛠️ **Tech Stack**

| **Layer**  | **Technology**                                                            |
| ---------- | ------------------------------------------------------------------------- |
| Frontend   | HTML, CSS, JavaScript                                                     |
| Backend    | Python (Flask, Flask-Session)                                             |
| Data Store | Local `words.json` (flat array or `{ "WORDS": [...] }`) of 5-letter words |
| Sessions   | Filesystem-based sessions via Flask-Session                               |

---

📁 **Folder Structure**

```
mini-wordle/
├── app.py             # Flask backend (loads words.json, handles /api/new and /api/guess)
├── index.html         # Single-page frontend (HTML + CSS + JS)
├── words.json         # Local JSON file containing the list of valid 5-letter words
├── requirements.txt   # pip dependencies: flask, flask-session
└── README.md          # Project documentation (this file)
```

* **`app.py`**

  * Loads `words.json` on startup, filters entries to exactly 5 alphabetical characters
  * `GET /` → Serves `index.html`
  * `GET /api/new` → Picks a random secret word, resets attempt counter
  * `POST /api/guess` → Accepts `{ "guess": "abcde" }`, returns feedback array (`["correct", "present", "absent", …]`) and game status (`"continue"`, `"win"`, `"lose"`)

* **`index.html`**

  * Renders a 6×5 grid of tiles and a 3-row on-screen keyboard (400 px wide)
  * Shortens “Enter” to “EN” and “Backspace” to “BS” for cleaner labels
  * Handles user input (clicks & keypresses), sends guesses via `fetch("/api/guess")`, and applies color feedback

* **`words.json`**

  * Must be a valid JSON file
  * Either a **flat array**:

    ```json
    [
      "apple",
      "bench",
      "crane",
      "delta",
      "eagle",
      "flute",
      "grace",
      "hound",
      "ivory",
      …
    ]
    ```
  * Or an **object** with a top-level “WORDS” key:

    ```json
    {
      "WORDS": [
        "which",
        "there",
        "their",
        "about",
        "would",
        "these",
        "other",
        "words",
        "could",
        …
      ]
    }
    ```

* **`requirements.txt`**

  ```txt
  Flask
  Flask-Session
  ```

---

🚀 **Getting Started**

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/mini-wordle.git
   cd mini-wordle
   ```

2. **(Optional) Create a virtual environment**

   ```bash
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows (PowerShell)
   python -m venv venv
   venv\Scripts\Activate.ps1

   # Windows (CMD)
   python -m venv venv
   venv\Scripts\activate.bat
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Verify your `words.json`**

   * Ensure it’s in the project root alongside `app.py`.
   * Confirm valid JSON syntax (no trailing commas!).
   * Either a flat array of 5-letter strings, or an object with a `"WORDS"` array.

5. **Run the Flask server**

   ```bash
   python app.py
   ```

   You should see:

   ```
   Loaded 5757 five-letter words from words.json.
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   ```

6. **Open your browser**
   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)
   → The game board loads, automatically calls `GET /api/new`, and you’re ready to play!

---

🎮 **Usage**

* Click or type letters to fill a row of 5 tiles.
* Hit **EN** (or press Enter) to submit your guess.
* Tiles will color:

  * 🟩 **Green** = correct letter & position
  * 🟨 **Yellow** = right letter, wrong position
  * ⬜ **Gray** = letter not in the word
* Use **BS** (or Backspace) to delete the last letter.
* Six guesses maximum. If you don’t guess in six tries, you lose and see `“Game over. Word was “_____””`.
* If you guess correctly, you see `“🎉 You guessed it!”`.
* Refresh the page to start a brand-new game with a fresh secret word.
