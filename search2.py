# import sqlite3

# # Search for a word in the SQLite database and print its definition
# def search_word_and_print_definition(word, database_name):
#     conn = sqlite3.connect(database_name)
#     cursor = conn.cursor()

#     # Perform a case-insensitive search for the word in the database
#     cursor.execute('SELECT definition FROM dictionary WHERE word LIKE ?', (word,))
#     result = cursor.fetchone()

#     conn.close()

#     if result:
#         definition = result[0]
#         print(f"Word: {word}")
#         print(f"Definition:\n{definition}")
#     else:
#         print(f"Word '{word}' not found in the dictionary.")

# # Example usage:
# database_name = 'dictionary2.db'  # Replace with the name of your SQLite database

# # Take user input for the word to search
# user_input = input("Enter a word to search: ")
# search_word_and_print_definition(user_input, database_name)


import json

class TrieNode:
    def __init__(self):
        self.children = {}
        self.definition = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, definition):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.definition = definition

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.definition

    def autocomplete(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._find_words_from_node(node, prefix)

    def _find_words_from_node(self, node, prefix):
        words = []
        if node.definition:
            words.append(prefix)
        for char, child_node in node.children.items():
            words.extend(self._find_words_from_node(child_node, prefix + char))
        return words

def load_dictionary(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def build_trie(dictionary_data):
    trie = Trie()
    for word, definition in dictionary_data.items():
        trie.insert(word.upper(), definition)  # Convert words to uppercase for case-insensitive search
    return trie

def search_word_and_print_definition(word, trie):
    word = word.upper()  # Convert the search word to uppercase for case-insensitive search
    definition = trie.search(word)
    if definition:
        print(f"Word: {word}")
        print(f"Definition:\n{definition}")
    else:
        print(f"Word '{word}' not found in the dictionary.")
        suggestions = trie.autocomplete(word)
        if suggestions:
            print("Did you mean:")
            for suggestion in suggestions:
                print(f" - {suggestion}")
        else:
            print("No suggestions found.")

# Load the dictionary data from the JSON file
json_file = 'dictionary2.json'  # Replace with your JSON file path
dictionary_data = load_dictionary(json_file)

# Build the Trie
trie = build_trie(dictionary_data)

# Take user input for the word to search
user_input = input("Enter a word to search: ")
search_word_and_print_definition(user_input, trie)
