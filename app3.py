from flask import Flask, render_template, request, session
import random
import requests
from unidecode import unidecode
from bs4 import BeautifulSoup
import csv
import unicodedata
from itertools import permutations
from urllib.parse import unquote


"""IDEES
- mettre un mode "sans limite de temps" sur la homepage et un mode "chrono" sur une autre
- mettre une option night mode"""

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
                        if span_fr.text == 'Forme de verbe':
                            span_desc = span_fr.find_next('li')
                            if span_desc and ('Participe passé' in span_desc.text or 'Participe présent' in span_desc.text):
                                all_spans_between.append('Participe')
                        else:
                            all_spans_between.append(span_fr.text)
                    elif span_class and 'sectionlangue' in span_class:
                        break
                    else:
                        """for heading in soup.find_all('span', class_='sectionlangue'):"""

    for span in all_spans_between:
        if span != 'Forme de verbe':
            isaword = True

    return isaword


def remove_accents(word):
    return ''.join(
        c for c in unicodedata.normalize('NFD', word)
        if unicodedata.category(c) != 'Mn'
    )


def generer_lettres():
    # Générer 6 lettres aléatoires en respectant la répartition voyelles/consonnes
    voyelles_disponibles = lettres['voyelles'] * nb_voyelles
    consonnes_disponibles = lettres['consonnes'] * nb_consonnes
    voyelles_tirees = random.sample(voyelles_disponibles, nb_voyelles)
    consonnes_tirees = random.sample(consonnes_disponibles, nb_consonnes)
    lettres_tirees = voyelles_tirees + consonnes_tirees
    random.shuffle(lettres_tirees)
    return lettres_tirees


def possiblecombinations(random_letters):
    #with open('words_length_5to10.txt', 'r', encoding='utf-8') as file:
    with open('words_output.csv', 'r', encoding='utf-8') as file:
        words = {remove_accents(word.strip()) for word in file}

    random_letters = [letter.lower() for letter in random_letters]

    print(random_letters)

    found_words = set()
    for r in range(5, 10):  # Range from 5 to 10 for word lengths
        for perm in permutations(random_letters, r):
            word = ''.join(perm)
            if word in words:
                found_words.add(word)

    # Initialize separate lists for word lengths from 5 to 10
    word_lists = {length: [] for length in range(5, 11)}

    for word in found_words:
        length = len(word)
        if 5 <= length <= 10:
            word_lists[length].append(word.upper())

    # Replace empty lists with "Aucun mot trouvé."
    for length, word_list in word_lists.items():
        if not word_list:
            word_lists[length] = ["Aucun mot trouvé."]

    return list(reversed(list(word_lists.items())))


def get_wiktionary_info(word_without_accents):
    search_url = f"https://fr.wiktionary.org/w/api.php?action=opensearch&search={word_without_accents}"
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        if data and len(data) >= 4:
            urls = data[3]
            if urls:
                for i in range(0,len(urls)):
                    last_url = urls[i]
                    last_word = last_url.split('/')[-1]
                    last_word_without_accents = unidecode(unquote(last_word))
                    print(last_word)
                    print(last_word_without_accents)
                    if last_word_without_accents == word_without_accents:
                        return unquote(last_word).upper()
    return False


@app.route('/', methods=['GET', 'POST'])
def index():
    error = ""

    if 'solution' not in session:
        session['solution'] = []

    if 'letters' not in session:
        session['letters'] = None

    # Vérifier si 'user_words' existe dans la session, sinon l'initialiser à une liste vide
    session['user_words'] = session.get('user_words', [])

    if request.method == 'GET':
        # Générer les lettres aléatoires
        session['letters'] = generer_lettres()
        session['user_words'] = []
        session['solutions'] = []
        return render_template('index3.html', letters=session['letters'], user_words=session['user_words'], error=error, solutions=[])

    if request.method == 'POST':
        if 'generate_lettres' in request.form:
            # Générer les lettres aléatoires
            session['letters'] = generer_lettres()
            session['user_words'] = []
            session['solution'] = []
            print(session)

        elif 'user_word' in request.form:
            # Récupérer le mot saisi par l'utilisateur et l'ajouter à la liste
            user_input = request.form['user_word'].strip()
            capitalized_session = [word.capitalize() for word in session['user_words']]
            if user_input.capitalize() not in capitalized_session:
                if check_letters(unidecode(user_input).upper(), session['letters']):
                    if doeswordexist(user_input.lower()):
                        session['user_words'].append(user_input.upper())
                        session['user_words'] = sorted(session['user_words'], key=len, reverse=True)
                    else:
                        if get_wiktionary_info(user_input):
                            session['user_words'].append(get_wiktionary_info(user_input))
                            session['user_words'] = sorted(session['user_words'], key=len, reverse=True)
                        else:
                            print(user_input, ": doeswordexist failed")
                            error = "Ce mot n'existe pas dans le dictionnaire de référence utilisé (" \
                                    "http://fr.wiktionary.org). "
                else:
                    print(user_input, ": check_letters failed")
                    error = "Le mot contient des lettres qui ne sont pas dans le tirage."
            else:
                error = "Vous avez déjà saisi ce mot."
            print(session)

        elif 'solution' in request.form:
            session['solution'] = possiblecombinations(session['letters'.lower()])
            print(session)

        return render_template('index3.html', letters=session['letters'], user_words=session['user_words'], error=error, solution=session['solution'])


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
    print(session)
