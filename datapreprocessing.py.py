# Read the Webster's dictionary text file
with open('utf.txt', 'r', encoding='utf-8') as file:
    websters_text = file.read()

# Split the text into lines to process each entry separately
entries = websters_text.split('\n')

# Initialize variables to store the extracted words and definitions
words_and_definitions = []

# Iterate through each entry in the dictionary
current_word = None
current_definition = ""
for line in entries:
    # Check if the line is a word (all uppercase letters)
    if line.isupper():
        # If we already have a current word, add it to the list
        if current_word:
            words_and_definitions.append((current_word, current_definition.strip()))
        
        # Set the new current word
        current_word = line.strip()
        current_definition = ""
    else:
        # Append the line to the current definition
        current_definition += line + '\n'

# Add the last word and definition to the list
if current_word:
    words_and_definitions.append((current_word, current_definition.strip()))

# Save the preprocessed data to a new text file
output_file = 'preprocessed_websters_dictionary.txt'
with open(output_file, 'w', encoding='utf-8') as outfile:
    for word, definition in words_and_definitions:
        # Write each word and definition to the output file
        outfile.write(f"Word: {word}\n")
        outfile.write(f"Definition: {definition}\n")
        outfile.write("-" * 30 + '\n')

# Print a message to indicate the data has been saved
print(f"Preprocessed data saved to {output_file}")
