import csv

with open(r'C:\Users\julien.mayzou\Documents\motlepluslong\outputxmltest1.csv', 'r', encoding='utf-8') as fichier:
    long_string = fichier.read()

with open(r'C:\Users\julien.mayzou\Documents\motlepluslong\outputxmltest2.csv', 'r', encoding='utf-8') as fichier:
    long_string = long_string + fichier.read()

with open(r'C:\Users\julien.mayzou\Documents\motlepluslong\outputxmltest3.csv', 'r', encoding='utf-8') as fichier:
    long_string = long_string + fichier.read()

with open(r'C:\Users\julien.mayzou\Documents\motlepluslong\outputxmltest4.csv', 'r', encoding='utf-8') as fichier:
    long_string = long_string + fichier.read()

with open(r'C:\Users\julien.mayzou\Documents\motlepluslong\outputxmltest5.csv', 'r', encoding='utf-8') as fichier:
    long_string = long_string + fichier.read()

# Split the string into a list of words
words_list = long_string.split(";")

# Define the output CSV file
output_file = "words_output.csv"

# Write the words into a CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    for word in words_list:
        csv_writer.writerow([word.strip()])  # Write each word into a separate row
