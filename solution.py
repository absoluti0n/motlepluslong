import requests
from bs4 import BeautifulSoup
import re
import time
import csv

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
                if span_fr:
                    span_class = span_fr.get('class')
                    if span_class and 'titredef' in span_class:
                        if "Forme de verbe" in span_fr.text:
                            span_verbe_def = span_fr.find_next('ol')
                            if span_verbe_def and "Participe passé" in span_verbe_def.text:
                                all_spans_between.append('Adjectif/Participe passé')
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


def is_french_word(word):
    # Define a regular expression pattern for French alphabet with accents
    pattern = re.compile(r'^[a-zA-ZÀ-ÿ]+$')

    # Check if the word matches the pattern
    return bool(re.match(pattern, word))


def is_first_letter_capitalized(s):
    return s[0].isupper() if s else False

start_time = time.time()

liste_words = []
index = 0

with open(r'C:\Users\julien.mayzou\Documents\motlepluslong\input4test.csv', 'r', encoding='utf-8') as fichier:
    # Lecture de chaque ligne du fichier
    #csv_reader = csv.reader(fichier, delimiter=';')
    csv_as_string = fichier.read()
    csv_reader = csv_as_string.split(';')

    for row in csv_reader:
        index += 1
        print(index)
        if doeswordexist(row):
                liste_words.append(row)


end_time = time.time()
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"Elapsed time: {elapsed_time} seconds")

# Writing the list to a CSV file with semicolons as separators
with open('output4frenchwords.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(liste_words)
    print(liste_words)
