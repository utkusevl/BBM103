import locale
import sys

# Set the locale to US English.
locale.setlocale(locale.LC_ALL, "en_US")

# Read the content of a file and return it, or None if the file is not found.
def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print("File not found")
        return None

# Count the total number of words and return the word count and cleaned word list.
def count_words(text):
    words = []
    for word in text.lower().split():
        cleaned_word = word.strip(".,!?;:()[]{}'\"")
        if cleaned_word:
            words.append(cleaned_word)
    return len(words), words

# Count the number of sentences by replacing punctuation and splitting the text.
def count_sentences(text):
    text = text.replace("...", ".").replace("?", ".").replace("!", ".")
    sentences = text.split('.')
    non_empty_sentences = []
    for sentence in sentences:
        if sentence.strip():
            non_empty_sentences.append(sentence)
    return len(non_empty_sentences)

# Calculate the average number of words per sentence.
def avg_words_per_sentence(word_count, sentence_count):
    return word_count / sentence_count

# Count the total number of characters in the text.
def count_characters(text):
    return len(text)

# Count the total number of characters in the cleaned word list.
def count_characters_in_words(words):
    total_length = 0
    for word in words:
        total_length += len(word)
    return total_length

# Calculate the frequency of each word in the word list.
def calculate_word_frequencies(words):
    freq = {}
    for word in words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    return freq

# Find the shortest words in the word list and their frequencies.
def find_shortest_words(words):
    word_count = calculate_word_frequencies(words)
    shortest_length = min(len(word) for word in words)

    shortest_words = {}
    for word in words:
        if len(word) == shortest_length:
            shortest_words[word] = word_count[word]

    shortest_words = dict(sorted(shortest_words.items(), key=lambda x: (-x[1], x[0])))

    return list(shortest_words.keys()), shortest_words

# Find the longest words in the word list and their frequencies.
def find_longest_words(words):
    word_count = calculate_word_frequencies(words)
    longest_length = max(len(word) for word in words)

    longest_words = {}
    for word in words:
        if len(word) == longest_length:
            longest_words[word] = word_count[word]

    longest_words = dict(sorted(longest_words.items(), key=lambda x: (-x[1], x[0])))

    return list(longest_words.keys()), longest_words

# Calculate and sort the word frequencies as percentages of the total word count.
def word_frequencies(words):
    word_count = calculate_word_frequencies(words)
    total_words = len(words)
    frequencies = {}
    for word, count in word_count.items():
        frequencies[word] = count / total_words
    sorted_frequencies = dict(sorted(frequencies.items(), key=lambda x: (-x[1], x[0])))
    return sorted_frequencies

# Analyze the text from a file, calculate statistics, and write results to an output file.
def analyze_and_write(input_path, output_path):
    content = read_file(input_path)
    if not content:
        return

    word_count, words = count_words(content)
    sentence_count = count_sentences(content)
    avg_words = avg_words_per_sentence(word_count, sentence_count)
    char_count = count_characters(content)
    char_count_in_words = count_characters_in_words(words)
    shortest_words, shortest_freq = find_shortest_words(words)
    longest_words, longest_freq = find_longest_words(words)
    frequencies = word_frequencies(words)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(f"Statistics about {input_path} :\n")
        file.write(f"#Words                  : {word_count}\n")
        file.write(f"#Sentences              : {sentence_count}\n")
        file.write(f"#Words/#Sentences       : {avg_words:.2f}\n")
        file.write(f"#Characters             : {char_count}\n")
        file.write(f"#Characters (Just Words): {char_count_in_words}\n")

        if len(shortest_freq) > 1:
            file.write("The Shortest Words      :\n")
        else:
            file.write("The Shortest Word       : ")
        for word, freq in shortest_freq.items():
            file.write(f"{word:24} ({freq / word_count:.4f})\n")

        if len(longest_freq) > 1:
            file.write("The Longest Words       :\n")
        else:
            file.write("The Longest Word        : ")
        for word, freq in longest_freq.items():
            file.write(f"{word:24} ({freq / word_count:.4f})\n")

        file.write("Words and Frequencies   :\n")
        word_items = list(frequencies.items())
        for word, freq in word_items[:-1]:
            file.write(f"{word:24}: {freq:.4f}\n")
        last_word, last_freq = word_items[-1]
        file.write(f"{last_word:24}: {last_freq:.4f}")

# Entry point for the program to analyze input and output file paths.
def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    analyze_and_write(input_path, output_path)

if __name__ == "__main__":
    main()