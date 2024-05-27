from flask import Flask, render_template, request, redirect, url_for
import csv

# import os
import random

app = Flask(__name__)

# Assuming vocabulary.csv is in the root directory
VOCABULARY_FILE = "./assets/Advanced Catalan_1.csv"


@app.route("/")
def start_game():
    # Load vocabulary from CSV
    vocabulary = []
    with open(VOCABULARY_FILE, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            vocabulary.append(row)

    # Randomly select a word
    selected_word = random.choice(vocabulary)
    return render_template(
        "game.html",
        word=selected_word[0],
        options=[option for option in selected_word[1:] if option != selected_word[0]],
    )


@app.route("/check_answer", methods=["POST"])
def check_answer():
    selected_option = request.form["option"]
    correct_option = request.args.get("correct_option")
    if selected_option == correct_option:
        return "Correct!"
    else:
        return "Incorrect."


if __name__ == "__main__":
    app.run(debug=True)
