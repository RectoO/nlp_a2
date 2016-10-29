import re
import codecs


def get_words_array(path):
    return remove_under_3(pre_process(path))


def get_sentence_array_process(path):
    return sentence_array(get_words_array(path))


def get_out_of_voc(path_train, path_test):
    train_word_array, unknown_list = remove_under_3(pre_process(path_train),
                                                    get_list=True)
    test_word_array = remove_unknown(pre_process(path_test), unknown_list)
    number = 0
    out_of_voc = set()
    word_dict = {}
    for word in train_word_array:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    print(len(train_word_array))
    print(len(test_word_array))
    for word in test_word_array:
        if word not in word_dict:
            number += 1
            out_of_voc.add(word)

    return number, out_of_voc


def get_sentence_no_unk(processed_train):
    return sentence_array(processed_train)


def get_sentences(processed_train, processed_test):
    word_array = remove_under_3(processed_train)
    train_array = sentence_array(word_array)
    test_word_array = remove_unknown(processed_test, set(word_array))
    test_array = sentence_array(test_word_array)

    return (train_array, test_array)


def pre_process(path):
    """
    Return an array of word in path. We first prune the file to remove noises
    """
    # Removed characters
    remove_char = ['"', '\'', ',', '‚', ';', '-', '(', ')', '$', '`', '*',
                   '&gt', 'frs.']
    # Removed section
    remove_section = [('\[', '\]'), ('<', '>')]
    # Dot regex
    dot_regex = "[a-zA-Z]*\.\.+[a-zA-Z]*"
    # Number regex
    number_regex = "[0-9]+"
    # Special rules
    remove_special = [(" &amp; ", "&"), ("mlle.", "mlle"), ("mr.", "mr"),
                      ("mme.", "mme"), ("lord.", "lord"), ("dr.", "dr"),
                      ("dom.", "dom")]
    # End tag
    end_tag = [("!", " </s> <s> "), ("?", " </s> <s> "), (".", " </s> <s> "),
               (":", " </s> <s> ")]

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

    # Replace number by <UNK> tag
    text = re.sub(number_regex, "<NBR>", text)

    # Applying the special replacements rules
    for (old, new) in remove_special:
        text = text.replace(old, new)

    # End Tag
    for (old, new) in end_tag:
        text = text.replace(old, new)

    # Start tag
    text = "<s> " + text

    # Every words in an array
    word_array = re.split("\s+", text.strip())

    # Remove last start tag if needed
    if word_array[-1] == '<s>':
        del word_array[-1]

    # Add a end tag if needed
    if word_array[-1] != '</s>':
        word_array.append('</s>')
    return word_array


def remove_under_3(word_array, get_list=False):
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

    if get_list:
        return word_array, replace_word
    else:
        return word_array


def remove_unknown(word_array, known_list):
    for x in range(0, len(word_array)):
        if word_array[x] not in known_list:
            word_array[x] = "<UNK>"

    return word_array


def sentence_array(word_array):
    # New sentence array
    sentence_array = []
    # Building sentence
    current_sentence = []
    # Iterate over every words
    for word in word_array:
        # If it's the end of a sentence
        if word == '</s>':
            # We end our current sentence
            current_sentence.append(word)
            # We add the sentence in our sentence array
            sentence_array.append(current_sentence[:])
            # We reste our current sentence
            current_sentence = []
        else:
            # We update our current sentence
            current_sentence.append(word)

    return sentence_array
