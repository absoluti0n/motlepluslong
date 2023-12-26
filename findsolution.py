import unicodedata
from unidecode import unidecode
import time
from itertools import product
import requests
from bs4 import BeautifulSoup
from itertools import permutations


start_time = time.time()

# Function to remove accents from words
def remove_accents(word):
    return ''.join(
        c for c in unicodedata.normalize('NFD', word)
        if unicodedata.category(c) != 'Mn'
    )


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


def possiblecombinations(random_letters):


    #with open('words_length_5to10.txt', 'r', encoding='utf-8') as file:
    with open('words_output.csv', 'r', encoding='utf-8') as file:
        words = {remove_accents(word.strip()) for word in file}

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
            word_lists[length].append(word)

    # Replace empty lists with "Aucun mot trouvé."
    for length, word_list in word_lists.items():
        if not word_list:
            word_lists[length] = "Aucun mot trouvé."

    return list(reversed(list(word_lists.items())))

random_letters = ['a','b','c','d','e','f','g','h','i','j']

for length, word_list in possiblecombinations(random_letters):
    print(f"{length} caractères: {word_list}")
#then check back the full words list to see if there are any accented words that match that list
#browse thru the xml files again and add the verbs with {{t|fr}}