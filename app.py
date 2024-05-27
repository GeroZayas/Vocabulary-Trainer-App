from flask import Flask, render_template
import csv
import random

app = Flask(__name__)

@app.route('/')
def quiz():
    # Read the CSV file with Catalan and English words
    words = []
    with open('words.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            words.append(row)

    # Select a random word pair
    word_pair = random.choice(words)
    catalan_word = word_pair[0]
    correct_translation = word_pair[1]

    # Shuffle the English translations
    translations = [pair[1] for pair in random.sample(words, 3)]
    translations.append(correct_translation)
    random.shuffle(translations)

    return render_template('quiz.html', catalan_word=catalan_word, translations=translations)

if __name__ == '__main__':
    app.run(debug=True)
