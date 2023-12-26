import csv
from collections import defaultdict

# Read the CSV file and group words by length
#word_groups = defaultdict(list)
word_groups = []

with open('words_output.csv', 'r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        word = row[0].strip()
        word_groups.append(word)

# Write each group of words to separate files
for words in word_groups:
    output_filename = f"words_length_5to10.txt"
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write(join(words))
