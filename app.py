from flask import Flask, render_template, request, redirect, url_for
import csv
import random
import os

app = Flask(__name__)

words = []
current_word_pair = ["one", "uno"]
correct_answers = 0
incorrect_answers = 0
words_seen = 0
percentage_correct = 0
selected_list = "Advanced Catalan"
uploaded_file_name = None


def load_words(file_path):
    global words
    words = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            words.append(row)


def get_new_word_pair():
    global current_word_pair
    current_word_pair = random.choice(words)
    return current_word_pair


def get_translations():
    translations = [pair[1] for pair in random.sample(words, 3)]
    translations.append(current_word_pair[1])
    random.shuffle(translations)
    return translations


@app.route("/")
def quiz():
    global selected_list
    if selected_list:
        load_words(f"assets/{selected_list}")
    else:
        load_words("assets/Advanced Catalan")
    get_new_word_pair()
    translations = get_translations()
    return render_template(
        "quiz.html",
        selected_list=selected_list,
        target_word=current_word_pair[0],
        translations=translations,
        correct_answers=correct_answers,
        incorrect_answers=incorrect_answers,
        words_seen=words_seen,
        percentage_correct=percentage_correct,
    )


@app.route("/check_answer", methods=["POST"])
def check_answer():
    global correct_answers, incorrect_answers, words_seen, percentage_correct
    selected_translation = request.form["selected_translation"]
    if selected_translation == current_word_pair[1]:
        message = random.choice(
            ["NICE!", "GOOD Job!", "You, genius!", "I mean... you goood!"]
        )
        correct_answers += 1
    else:
        message = random.choice(
            ["Wrong!", "Not quite!", "Well, not exactly", "You can do better!"]
        )
        incorrect_answers += 1
    words_seen += 1
    new_word_pair = get_new_word_pair()
    translations = get_translations()

    percentage_correct = (
        int((correct_answers / words_seen) * 100) if words_seen > 0 else 0
    )

    return render_template(
        "quiz.html",
        selected_list=(
            selected_list[:-4] if selected_list.endswith("csv") else selected_list
        ),
        target_word=new_word_pair[0],
        translations=translations,
        message=message,
        correct_answers=correct_answers,
        incorrect_answers=incorrect_answers,
        words_seen=words_seen,
        percentage_correct=percentage_correct,
    )


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    global uploaded_file_name
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == "":
            return "No file selected"
        if file:
            uploaded_file_name = file.filename
            file.save(f"assets/{uploaded_file_name}")
            load_words(f"assets/{uploaded_file_name}")
            return "File uploaded successfully"
    return render_template("upload.html")


@app.route("/choose_list", methods=["GET", "POST"])
def choose_list():
    global selected_list
    if request.method == "POST":
        selected_list = request.form["selected_list"]
        load_words(f"assets/{selected_list}")
        return redirect("/")
    files = os.listdir("assets")
    return render_template("choose_list.html", files=files)


@app.route("/create")
def create_list():
    return render_template("create_list.html")


@app.route("/save_list", methods=["POST"])
def save_list():
    list_name = request.form["list_name"]
    word_pairs = request.form["word_pairs"].split("\n")
    file_path = f"assets/{list_name}.csv"
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        for pair in word_pairs:
            word, translation = pair.strip().split(",")
            writer.writerow([word, translation])
    return redirect("/choose_list")


if __name__ == "__main__":
    app.run(debug=True)
