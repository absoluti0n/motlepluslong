import re
import time
import csv
from lxml import etree


def is_french_word(word):
    # Define a regular expression pattern for French alphabet with accents
    pattern = re.compile(r'^[a-zA-ZÀ-ÿ]+$')

    # Check if the word matches the pattern
    return bool(re.match(pattern, word))


def remove_accents(word):
    return ''.join(
        c for c in unicodedata.normalize('NFD', word)
        if unicodedata.category(c) != 'Mn'
    )


def is_first_letter_capitalized(s):
    return s[0].isupper() if s else False


start_time = time.time()

# Define the file path
file_path = r"C:\Users\julien.mayzou\Downloads\frwiktionary-20231220-pages-articles-multistream.xml"

#tree = etree.parse(r"C:\Users\julien.mayzou\Downloads\frwiktionary-20231220-pages-articles-multistream-sample.xml")
#root = tree.getroot()

# Define your XML file path

xml_file = r"C:\Users\julien.mayzou\Downloads\xmlwiktionary\frwiktionary-20231220-pages-articles-multistreamheadereditupto36280961.xml"

liste_mots = []
itero = 0

for event, element in etree.iterparse(xml_file, events=("start", "end")):
    #if itero < 10000:
        if event == "end" and element.tag.endswith("page"):
            title_element = element.find("title")
            if title_element is not None:
                title = title_element.text
                if is_french_word(title) and not is_first_letter_capitalized(title) and len(title)>4 and len(title)<11:
                    text_element = element.find(".//text")
                    if text_element is not None:
                        text = text_element.text
                        if text and "{{langue|fr}}" in text:
                            if "=== {{S|verbe|fr" in text and any(subtag in text for subtag in ["{{t|fr}}"]):
                                liste_mots.append(title)
            element.clear()


"""for page in root.findall('page'):
    title = page.find('title').text
    print(title)
    if is_french_word(title):
        if not is_first_letter_capitalized(title):
            text = page.find(".//text").text
            #match = re.search(lpattern, text)
            if "{{langue|fr}}" in text:
                if "=== {{S|nom|fr" in text or "=== {{S|adjectif|fr" in text or "=== {{S|adverbe|fr" in text or "=== " \
                                               "{{S|pronom|fr" in text:
                    liste_mots.append(title)
                elif "=== {{S|verbe|fr" in text:
                    if "ppr=oui}}" in text or "ppfp=oui}}" in text or "{{i|fr}}" in text:
                        liste_mots.append(title)"""

print(liste_mots)

end_time = time.time()
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"Elapsed time: {elapsed_time} seconds")

# Writing the list to a CSV file with semicolons as separators
with open('outputxmltest10.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(liste_mots)
