from flask import Flask, render_template, request
import random

app = Flask(__name__)

lettres = {
    'voyelles': 'AEIOUY',
    'consonnes': 'BCDFGHJKLMNPQRSTVWXZ'
}

nb_consonnes = 6
nb_voyelles = 4

def generer_lettres():
    # Générer 6 lettres aléatoires en respectant la répartition voyelles/consonnes
    voyelles_disponibles = lettres['voyelles'] * nb_voyelles
    consonnes_disponibles = lettres['consonnes'] * nb_consonnes
    voyelles_tirees = random.sample(voyelles_disponibles, nb_voyelles)
    consonnes_tirees = random.sample(consonnes_disponibles, nb_consonnes)
    lettres_tirees = voyelles_tirees + consonnes_tirees
    random.shuffle(lettres_tirees)
    return lettres_tirees

@app.route('/', methods=['GET', 'POST'])
def index():
    lettres_tirees = None
    user_input = None

    if request.method == 'POST':
        if 'generate_lettres' in request.form:
            # Logic to generate lettres
            lettres_tirees = generer_lettres()

        elif 'user_word' in request.form:
            # Process user input for the word
            user_input = request.form['user_word']

    return render_template('index2.html', letters=lettres_tirees, user_input=user_input)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)