from flask import Flask, render_template, request, session
import random
import requests
from unidecode import unidecode
from bs4 import BeautifulSoup
import csv

"""IDEES
- mettre un mode "sans limite de temps" sur la homepage et un mode "chrono" sur une autre
- mettre une option night mode
- mettre un lien vers github / contact
- mettre un weighting à chaque lettre pour le tirage, pour avoir plus de E etc
- bouton solution / changer de layout pour avoir une liste des mots les plus longs avec ce tirage"""

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

lettres_unweighted = {
    'voyelles': 'AEIOUY',
    'consonnes': 'BCDFGHJKLMNPQRSTVWXZ'
}

with open('letter_weighting.csv', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';')
    letter_weighting = {}
    for row in csv_reader:
        letter_weighting[row[0]] = row[1]

lettres = {
    'voyelles': '',
    'consonnes': ''
}

for lettre_type in lettres_unweighted:
    for lettre in lettres_unweighted[lettre_type]:
        lettres[lettre_type] = lettres[lettre_type] + lettre * int(letter_weighting[lettre])

nb_consonnes = 5
nb_voyelles = 5


def check_letters(word_a, word_b):
    # Create dictionaries to count occurrences of each letter in words A and B
    count_a = {}
    count_b = {}

    # Count occurrences of each letter in word A
    for letter in word_a:
        count_a[letter] = count_a.get(letter, 0) + 1

    # Count occurrences of each letter in word B
    for letter in word_b:
        count_b[letter] = count_b.get(letter, 0) + 1

    # Check if each letter in word A is present in word B and not used more times than available
    for letter, count in count_a.items():
        if letter not in count_b or count > count_b[letter]:
            return False

    if len(word_a) < 3:
        print("Le mot est trop court.")
        return False

    return True


def doeswordexist(word):
    url = 'https://fr.wiktionary.org/wiki/'
    isaword = False

    # Faire une requête GET à l'URL
    response = requests.get(url + word)

    all_spans_between = []

    if response.status_code == 200:
        # Analyser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Trouver l'élément <span> avec id="fr"
        span_fr = soup.find('span', id='fr')

        if span_fr:
            while span_fr:
                span_fr = span_fr.find_next('span')
                # print(span_fr)
                if span_fr:
                    span_class = span_fr.get('class')
                    if span_class and 'titredef' in span_class:
                        all_spans_between.append(span_fr.text)
                    elif span_class and 'sectionlangue' in span_class:
                        break
                    else:
                        """for heading in soup.find_all('span', class_='sectionlangue'):"""

    for span in all_spans_between:
        if span != 'Forme de verbe':
            isaword = True

    return isaword


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
    error = ""

    if 'letters' not in session:
        session['letters'] = None

    # Vérifier si 'user_words' existe dans la session, sinon l'initialiser à une liste vide
    session['user_words'] = session.get('user_words', [])

    if request.method == 'GET':
        # Générer les lettres aléatoires
        session['letters'] = generer_lettres()
        session['user_words'] = []
        return render_template('index3.html', letters=session['letters'], user_words=session['user_words'], error=error)

    if request.method == 'POST':
        if 'generate_lettres' in request.form:
            # Générer les lettres aléatoires
            session['letters'] = generer_lettres()
            session['user_words'] = []

        elif 'user_word' in request.form:
            # Récupérer le mot saisi par l'utilisateur et l'ajouter à la liste
            user_input = request.form['user_word']
            capitalized_session = [word.capitalize() for word in session['user_words']]
            if user_input.capitalize() not in capitalized_session:
                if check_letters(unidecode(user_input).upper(), session['letters']):
                    if doeswordexist(user_input.lower()):
                        session['user_words'].append(user_input.capitalize())
                        session['user_words'] = sorted(session['user_words'], key=len, reverse=True)
                    else:
                        print(user_input, ": doeswordexist failed")
                        error = "Ce mot n'existe pas dans le dictionnaire de référence utilisé (" \
                                "http://fr.wiktionary.org). "
                else:
                    print(user_input, ": check_letters failed")
                    error = "Mot invalide."
            else:
                error = "Vous avez déjà saisi ce mot."
            print(session)
        return render_template('index3.html', letters=session['letters'], user_words=session['user_words'], error=error)


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
    print(session)
