import json

# Load the dictionary data from the JSON file
def load_dictionary(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        dictionary = json.load(file)
    return dictionary

# Search for a word in the dictionary and print its definition
def search_word_and_print_definition(word, dictionary):
    word = word.upper()  # Convert the search word to uppercase for case-insensitive search
    if word in dictionary:
        definition = dictionary[word]
        print(f"Word: {word}")
        print(f"Definition:\n{definition}")
    else:
        print(f"Word '{word}' not found in the dictionary.")

# Example usage:
json_file = 'dictionary2.json'  # Replace with your JSON file path
dictionary_data = load_dictionary(json_file)

# Take user input for the word to search
user_input = input("Enter a word to search: ")
search_word_and_print_definition(user_input, dictionary_data)
