from flask import Flask, request, jsonify
import random
import requests
from unidecode import unidecode
from bs4 import BeautifulSoup

app = Flask(__name__)

# Générer des voyelles et des consonnes avec leurs fréquences respectives
lettres = {
    'voyelles': 'AEIOUY',
    'consonnes': 'BCDFGHJKLMNPQRSTVWXZ'
}

nb_consonnes = 6
nb_voyelles = 4

timelimit = 15


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


@app.route('/generer-lettres', methods=['GET'])
def generer_lettres():
    # Générer 6 lettres aléatoires en respectant la répartition voyelles/consonnes
    voyelles_disponibles = lettres['voyelles'] * nb_voyelles
    consonnes_disponibles = lettres['consonnes'] * nb_consonnes
    voyelles_tirees = random.sample(voyelles_disponibles, nb_voyelles)
    consonnes_tirees = random.sample(consonnes_disponibles, nb_consonnes)
    lettres_tirees = voyelles_tirees + consonnes_tirees
    random.shuffle(lettres_tirees)
    return lettres_tirees

@app.route('/check-letters', methods=['POST'])
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


@app.route('/get-user-input', methods=['POST'])
def get_user_input():
    return input("Formez un mot avec ces lettres : ").upper()


@app.route('/doeswordexist',methods=['POST'])
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
                        # print("Class of 'yo' is not 'titredef'")
                        # ok = soup.find(class_="sectionlangue").text
                        # print(ok)
                        """for heading in soup.find_all('span', class_='sectionlangue'):
                            #putain.append = heading.text
                            print(heading)
                            for sibling in heading.find_next_siblings(attrs=):
                                if sibling.name == 'sectionlangue':
                                    break
                                elif sibling.name == 'titredef':
                                    values.append(sibling.text)
                                values.append(sibling.text)
                            blocks[heading.text] = values"""

        """else:
            print('Balise span avec id="fr" non trouvée')
    else:
        print('Échec de la récupération de la page')"""

    for span in all_spans_between:
        if span != 'Forme de verbe':
            isaword = True

    return(isaword)

@app.route('/main')
def main():
    lettres_tirees = generer_lettres()
    lettres_tirees_str = ' '.join(lettres_tirees)
    print(f"Voici les lettres disponibles : {lettres_tirees_str}")

    mot_utilisateur = get_user_input()

    mot_utilisateur_sans_accent = unidecode(mot_utilisateur)

    while not check_letters(mot_utilisateur_sans_accent, lettres_tirees):
        print("Mot invalide.")
        mot_utilisateur = get_user_input()
        mot_utilisateur_sans_accent = unidecode(mot_utilisateur)
    else:
        while not doeswordexist(mot_utilisateur.lower()):
            print("Mot existe pas.")
            mot_utilisateur = get_user_input()
            mot_utilisateur_sans_accent = unidecode(mot_utilisateur)
        else:
            print("Le mot est valide")


@app.route("/main")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host='localhost',port=5000,debug=True)