from flask import Flask, render_template, request
import random

app = Flask(__name__)

lettres = {
    'voyelles': 'AEIOUY',
    'consonnes': 'BCDFGHJKLMNPQRSTVWXZ'
}

nb_consonnes = 6
nb_voyelles = 4


@app.route('/', methods=['GET'])
def generer_lettres():
    # Générer 6 lettres aléatoires en respectant la répartition voyelles/consonnes
    voyelles_disponibles = lettres['voyelles'] * nb_voyelles
    consonnes_disponibles = lettres['consonnes'] * nb_consonnes
    voyelles_tirees = random.sample(voyelles_disponibles, nb_voyelles)
    consonnes_tirees = random.sample(consonnes_disponibles, nb_consonnes)
    lettres_tirees = voyelles_tirees + consonnes_tirees
    random.shuffle(lettres_tirees)
    #return lettres_tirees
    return render_template('input_form.html', letters=lettres_tirees)


# This will be the main route
@app.route('/', methods=['GET', 'POST'])
def process_input():
    user_input = ''
    if request.method == 'POST':
        user_input = request.form['user_input']
    return render_template('input_form.html', user_input=user_input)


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
