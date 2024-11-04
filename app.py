from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Trie data structure for autocomplete
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def autocomplete(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._find_words_from_node(node, prefix)

    def _find_words_from_node(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)
        for char, child_node in node.children.items():
            words.extend(self._find_words_from_node(child_node, prefix + char))
        return words

# Function to load words from the database into the Trie
def load_words_into_trie():
    trie = Trie()
    conn = sqlite3.connect('dictionary2.db')
    cursor = conn.cursor()
    cursor.execute('SELECT word FROM dictionary')
    words = cursor.fetchall()
    for word_tuple in words:
        word = word_tuple[0].lower()  # Make words lowercase to handle case-insensitive search
        trie.insert(word)
    conn.close()
    print("Trie loaded with words")  # Debug print
    return trie


# Build the Trie on startup
trie = load_words_into_trie()

# Function to search for a word in the SQLite database
def search_word_in_database(word):
    conn = sqlite3.connect('dictionary2.db')
    cursor = conn.cursor()
    cursor.execute('SELECT definition FROM dictionary WHERE word LIKE ?', (word,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    word = request.form.get('word')
    definition = search_word_in_database(word)
    if definition:
        return render_template('results.html', query=word, definition=definition)
    else:
        return render_template('results.html', query=word, definition='Word not found')

# Autocomplete endpoint
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    prefix = request.args.get('prefix', '').lower()  # Get prefix from query string
    suggestions = trie.autocomplete(prefix)[:5]  # Limit to top 5 suggestions
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
