from flask import Flask, render_template, request, jsonify
import sqlite3
import heapq

app = Flask(__name__)

# Trie data structure for autocomplete
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.definition = None
        self.frequency = 0  # Add frequency counter

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.max_heap = []  # Max-heap to store the most frequently searched words

    def insert(self, word, definition):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.definition = definition
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        if node.is_end_of_word:
            node.frequency += 1  # Increment frequency counter
            heapq.heappush(self.max_heap, (-node.frequency, word))  # Push to max-heap
            return node.definition
        return None

    def autocomplete(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        words = self._find_words_from_node(node, prefix)
        # Sort words by frequency in descending order
        words.sort(key=lambda x: -x[1])
        return [word for word, _ in words]

    def _find_words_from_node(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append((prefix, node.frequency))
        for char, child_node in node.children.items():
            words.extend(self._find_words_from_node(child_node, prefix + char))
        return words

    def get_most_frequent_words(self, k):
        # Get the top k most frequently searched words
        return heapq.nsmallest(k, self.max_heap)

# Function to load words from the database into the Trie
def load_words_into_trie():
    trie = Trie()
    conn = sqlite3.connect('dictionary2.db')
    cursor = conn.cursor()
    cursor.execute('SELECT word, definition FROM dictionary')
    words = cursor.fetchall()
    for word_tuple in words:
        word = word_tuple[0].lower()  # Make words lowercase to handle case-insensitive search
        definition = word_tuple[1]
        trie.insert(word, definition)
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
    word = request.form.get('word').lower()
    definition = trie.search(word)
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

# Most frequent words endpoint
@app.route('/most_frequent', methods=['GET'])
def most_frequent():
    k = int(request.args.get('k', 5))  # Get the number of most frequent words to return
    most_frequent_words = trie.get_most_frequent_words(k)
    return jsonify([word for _, word in most_frequent_words])

if __name__ == '__main__':
    app.run(debug=True)