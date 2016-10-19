import re
import codecs


def get_words_array(path):
    return remove_under_3(pre_process(path))


def pre_process(path):
    """
    Return an array of word in path. We first prune the file to remove noises
    """
    # Removed characters
    remove_char = ['"', '\'', ',', '‚', ';', '-', '(', ')', '$', '`', '*',
                   '&gt', 'Frs.', 'frs.']
    # Removed section
    remove_section = [('\[', '\]'), ('<', '>')]
    # Dot regex
    dot_regex = "[a-zA-Z]*\.\.+[a-zA-Z]*"
    # Number regex
    number_regex = "[0-9]+"
    # Special rules
    remove_special = [(" &amp; ", "&"), ("!", " <ES> "), ("?", " <ES> "),
                      (".", " <ES> "), (":", " <ES> "), ("Mlle.", "Mlle"),
                      ("Mr.", "Mr"), ("Mme.", "Mme"), ("Lord.", "Lord"),
                      ("Dr.", "Dr"), ("Dom.", "Dom")]

    # Read the file
    with codecs.open(path, "r", encoding='utf-8', errors='ignore') as f:
        text = f.read().lower()

    # Remove the useless characters
    for char in remove_char:
        text = text.replace(char, "")

    # Remove the useless sections
    for (begin, end) in remove_section:
        text = re.sub("("+begin+")(.)*("+end+")", "", text)

    # Replace dot dot dot by <UNK> tag
    text = re.sub(dot_regex, "<UNK>", text)

    # Replace dot dot dot by <UNK> tag
    text = re.sub(number_regex, "<NBR>", text)

    # Applying the special replacements rules
    for (old, new) in remove_special:
        text = text.replace(old, new)

    # Return the words of the text in array
    return re.split("\s+", text)


def remove_under_3(word_array):
    word_dict = {}
    for word in word_array:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1

    replace_word = set()
    for key, value in word_dict.items():
        if value < 3:
            replace_word.add(key)

    for x in range(0, len(word_array)):
        if word_array[x] in replace_word:
            word_array[x] = "<UNK>"

    return word_array


def n_gram(word_array, n):
    unigram = dict()

    for wordIndex in range(0, len(word_array)-(n-1)):
        word = list()
        for x in range(0, n):
            word.append(word_array[(wordIndex + x)])

        wordHash = str(word)
        if wordHash in unigram:
            unigram[wordHash] += 1
        else:
            unigram[wordHash] = 1

    return unigram


def ngram_occurence(ngram_dict):
    occurence_dict = dict()
    for key, value in ngram_dict.items():
        if value in occurence_dict:
            occurence_dict[value] += 1
        else:
            occurence_dict[value] = 1

    return occurence_dict


def prediction_dictionnary(word_array, n):
    pred_dict = dict()
    current_dict = dict()

    for x in range(n, len(word_array)):
        current_dict = pred_dict
        for y in range(n, 0, -1):
            wordIndex = x-y

            if word_array[wordIndex] in current_dict:
                current_dict = current_dict[word_array[wordIndex]]
            else:
                current_dict[word_array[wordIndex]] = dict()
                current_dict = current_dict = current_dict[word_array[wordIndex]]

        if word_array[x] in current_dict:
            current_dict[word_array[x]] += 1
        else:
            current_dict[word_array[x]] = 1

    return pred_dict
