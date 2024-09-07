import csv

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        words = text.split()
        return set(words)

def read_csv_file(file_path):
    words = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            for word in row:
                words.add(word)
    return words

def find_common_words(text_file_path, csv_file_path):
    text_words = read_text_file(text_file_path)
    csv_words = read_csv_file(csv_file_path)
    
    common_words = text_words.intersection(csv_words)
    
    return common_words

text_file_path = 'C:\\Users\\vishn\\Project_Notify\\result.txt'
csv_file_path = 'C:\\Users\\vishn\\Project_Notify\\sadwords.csv'

common_words = find_common_words(text_file_path, csv_file_path)

print("Common words found:")
for word in common_words:
    print(word)