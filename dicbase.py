import sqlite3
import json

# Load the dictionary data from the JSON file
def load_dictionary(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        dictionary = json.load(file)
    return dictionary

# Save the dictionary data to an SQLite database
def save_to_database(data, database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Create a table to store the dictionary data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dictionary (
            word TEXT PRIMARY KEY,
            definition TEXT
        )
    ''')

    # Insert or replace the dictionary data into the table
    for word, definition in data.items():
        cursor.execute('INSERT OR REPLACE INTO dictionary (word, definition) VALUES (?, ?)', (word, definition))

    conn.commit()
    conn.close()

#  usage
if __name__ == "__main__":
    json_file = 'dictionary2.json'
    database_name = 'dictionary.db'
    dictionary_data = load_dictionary(json_file)
    save_to_database(dictionary_data, database_name)

print(f'Dictionary data saved to {database_name}.')
