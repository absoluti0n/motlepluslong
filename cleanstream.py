import re
import time
import csv


def is_french_word(word):
    # Define a regular expression pattern for French alphabet with accents
    pattern = re.compile(r'^[a-zA-ZÀ-ÿ]+$')

    # Check if the word matches the pattern
    return bool(re.match(pattern, word))


def is_first_letter_capitalized(s):
    return s[0].isupper() if s else False

liste_words = []
start_time = time.time()


with open(r'C:\Users\julien.mayzou\Downloads\frwiktionary-20231220-pages-articles-multistream-index2.txt', 'r', encoding='utf-8') as fichier:
    # Lecture de chaque ligne du fichier
    for ligne in fichier:
        # Séparation de la ligne en ses éléments individuels
        elements = ligne.strip().split(':')

        # Vérification si la ligne a bien 3 éléments (stream, id, mot)
        if len(elements) == 3:
            #if len(elements[2]) > 4 and len(elements)<11:
            if len(elements[2]) == 4:
                if is_french_word(elements[2]):
                    if not is_first_letter_capitalized(elements[2]):
                        liste_words.append(elements[2])


end_time = time.time()
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"Elapsed time: {elapsed_time} seconds")

# Writing the list to a CSV file with semicolons as separators
with open('output4.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(liste_words)
