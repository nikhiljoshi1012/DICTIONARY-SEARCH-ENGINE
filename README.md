# Dictionary Search Engine 📚

A dictionary search engine built to efficiently parse, store, and search for words and their definitions. This project leverages text parsing, JSON storage, SQLite for database management, and Flask for a simple yet effective web interface.

## Features

- **Parsing and Extraction**: Downloads and parses the Webster's dictionary text file (UTF plain text version) to extract words along with their definitions.
- **Data Structuring**: Tokenizes the text, separating words from their meanings, and stores them as key-value pairs (word: definition) in a Python dictionary.
- **JSON Storage**: Saves the structured dictionary to a `dictionary2.json` file.
- **Database Integration**: Loads the JSON data into an SQLite database, creating a table with two columns for word and definition.
- **Searchable Web Interface**: Uses Flask to create a simple webpage where users can search for words directly from the database.

## Installation and Usage

Follow these steps to get the Dictionary Search Engine up and running:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/nikhiljoshi1012/DICTIONARY-SEARCH-ENGINE.git
   cd DICTIONARY-SEARCH-ENGINE
   ```

2. **Install Dependencies**: Install the required Python packages by running:

   ```bash
   pip install -r requirements.txt
   ```

3. **Parse the Dictionary and Load Database**: Run the script to parse the dictionary text file and populate the SQLite database:

   ```bash
   python parse_dictionary.py
   ```

4. **Start the Flask Web Server**: Launch the web server to access the dictionary search engine:

   ```bash
   flask run
   ```

5. **Access the Search Engine**: Open your browser and go to `http://127.0.0.1:5000` to start searching for words.

## Project Structure

- `parse_dictionary.py`: The script that processes the dictionary file, extracts words and definitions, saves them in `dictionary2.json`, and loads them into the SQLite database.
- `dictionary2.json`: JSON file that stores the words and definitions in key-value format.
- `database.db`: SQLite database containing a words table with word and definition columns.
- **Flask Application**: Provides a simple web-based interface for searching words in the database.

## Contributing

Contributions are encouraged! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Open a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License.

For more information, feel free to explore the repository or reach out with questions. Enjoy building your own dictionary search engine!
