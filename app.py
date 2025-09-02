from flask import Flask, render_template, request, jsonify
import random
import requests

app = Flask(__name__)

# Fetch words from GitHub raw link
URL = "https://gist.githubusercontent.com/dracos/dd0668f281e685bad51479e5acaadb93/raw/6bfa15d263d6d5b63840a8e5b64e04b382fdb079/valid-wordle-words.txt"
response = requests.get(URL)
WORDS = response.text.splitlines()  # list of words

def filter_words(possible_words, guess, feedback):
    new_list = []
    for word in possible_words:
        match = True
        for i, (g, f) in enumerate(zip(guess, feedback)):
            if f == "🟩" and word[i] != g:
                match = False
            elif f == "🟨" and (g not in word or word[i] == g):
                match = False
            elif f == "⬛" and g in word:
                match = False
        if match:
            new_list.append(word)
    return new_list

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/guess", methods=["POST"])
def guess():
    data = request.json
    guess_word = data["guess"].lower()
    feedback = data["feedback"]
    
    if "possible_words" in data and data["possible_words"]:
        possible_words = data["possible_words"]
    else:
        possible_words = WORDS
    
    possible_words = filter_words(possible_words, guess_word, feedback)
    next_guess = random.choice(possible_words) if possible_words else "-----"
    
    return jsonify({"next_guess": next_guess, "possible_words": possible_words})

if __name__ == "__main__":
    app.run(debug=True)
