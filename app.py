from flask import Flask, render_template, request
import csv
import random

app = Flask(__name__)

words = []
current_word_pair = None
correct_answers = 0
incorrect_answers = 0
words_seen = 0

def load_words():
    global words
    with open('assets/Advanced Catalan_1.csv', 'r') as file:
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

@app.route('/')
def quiz():
    load_words()
    get_new_word_pair()
    translations = get_translations()
    return render_template('quiz.html', catalan_word=current_word_pair[0], translations=translations, correct_answers=correct_answers, incorrect_answers=incorrect_answers, words_seen=words_seen)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    global correct_answers, incorrect_answers, words_seen
    selected_translation = request.form['selected_translation']
    if selected_translation == current_word_pair[1]:
        message = 'NICE!'
        correct_answers += 1
    else:
        message = 'Wrong!'
        incorrect_answers += 1
    words_seen += 1
    new_word_pair = get_new_word_pair()
    translations = get_translations()

    percentage_correct = (correct_answers / words_seen) * 100 if words_seen > 0 else 0

    return render_template('quiz.html', catalan_word=new_word_pair[0], translations=translations, message=message, correct_answers=correct_answers, incorrect_answers=incorrect_answers, words_seen=words_seen, percentage_correct=percentage_correct)

if __name__ == '__main__':
    app.run(debug=True)
