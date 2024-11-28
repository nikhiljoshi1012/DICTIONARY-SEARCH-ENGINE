from flask import Flask, render_template, request, jsonify
import sqlite3
import heapq
import time 
app = Flask(__name__)

# Trie data structure for autocomplete
class TrieNode:
    def __init__(self):
        self.children = {} #Dictionary to store child nodes.
        self.is_end_of_word = False #Boolean to mark the end of a word
        self.definition = None
        self.frequency = 0  # Add frequency counter

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.max_heap = []  # Max-heap to store the most frequently searched words

#Adds word and its definition to the trie
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
        return heapq.nsmallest(k, self.max_heap) #max-heap

# Levenshtein Distance algorithm to find the closest match for misspellings
def levenshtein_distance(word1, word2):
    dp = [[0] * (len(word2) + 1) for _ in range(len(word1) + 1)]

    for i in range(len(word1) + 1):
        for j in range(len(word2) + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[-1][-1]

# Function to find the closest word using Levenshtein Distance
def find_closest_word(trie, word, max_candidates=100):
    # Get a subset of words based on the prefix
    prefix = word[:4]  # Adjust the prefix length as needed
    candidate_words = trie.autocomplete(prefix)
    
    # If the number of candidates is too large, limit it
    if len(candidate_words) > max_candidates:
        candidate_words = candidate_words[:max_candidates]
    
    closest_word = None
    min_distance = float('inf')

    for w in candidate_words:
        distance = levenshtein_distance(word, w)
        if distance < min_distance:
            min_distance = distance
            closest_word = w

    return closest_word

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
    start_time = time.perf_counter()  # Start high-resolution timing

    definition = trie.search(word)

    elapsed_time = (time.perf_counter() - start_time) * 1000  # Elapsed time in milliseconds

    if definition:
        return render_template('results.html', query=word, definition=definition, elapsed_time=elapsed_time)
    else:
        closest_word = find_closest_word(trie, word)
        if closest_word:
            closest_definition = trie.search(closest_word)
            return render_template('results.html', query=word, definition=None, closest_word=closest_word, closest_definition=closest_definition, elapsed_time=elapsed_time)
        return render_template('results.html', query=word, definition='Word not found', elapsed_time=elapsed_time)
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
    app.run(debug=True,host='0.0.0.0')