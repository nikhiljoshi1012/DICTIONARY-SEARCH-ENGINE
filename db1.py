# Define a function to extract words and definitions from the dictionary text
def extract_words_and_definitions(file_path):
    words_and_definitions = []  # List to store extracted word-definition pairs
    current_word = None  # Variable to store the current word
    current_definition = None  # Variable to store the current definition
    in_definition_section = False  # Flag to indicate if we are in the definition section

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace

            # Check if the line contains all capital letters (potential word)
            if line.isupper():
                if current_word:
                    # Store the previous word-definition pair
                    words_and_definitions.append({'word': current_word, 'definition': current_definition})
                # Set the current word and reset the definition
                current_word = line
                current_definition = None
                in_definition_section = False
            elif "definition" in line.lower():
                # We have entered the definition section
                in_definition_section = True
                # Start collecting the definition text
                current_definition = line
            elif in_definition_section:
                # Collect lines within the definition section
                current_definition += '\n' + line

    # Add the last word-definition pair (if any) to the list
    if current_word:
        words_and_definitions.append({'word': current_word, 'definition': current_definition})

    return words_and_definitions

# Example usage:
file_path = 'utf.txt'  # Replace with your dictionary file path
result = extract_words_and_definitions('db.txt')

# Print the extracted word-definition pairs
for item in result:
    print("Word:", item['word'])
    print("Definition:", item['definition'])
    print("\n")
