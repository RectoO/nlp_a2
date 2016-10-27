import re
import codecs
import json
import math


def get_words_array(path):
    return remove_under_3(pre_process(path))


def get_sentence_array_process(path):
    return sentence_array(get_words_array(path))


def get_sentence_array(path_train, path_test):
    word_array, unknown_list = remove_under_3(pre_process(path_train), get_list=True)
    train_array = sentence_array(word_array)
    test_word_array = remove_unknown(pre_process(path_test), unknown_list)
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


def remove_unknown(word_array, unknown_list):
    for x in range(0, len(word_array)):
        if word_array[x] in unknown_list:
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


def prediction_dictionnary(sentence_list, n):
    pred_dict = dict()
    # We built the dictionnary for each sentence
    for sentence in sentence_list:
        # We iterate trought the words of the sentence
        for x in range(1, len(sentence)):
            # We create a list of the previous word for the current word
            list_previous_word = list()
            for y in range(x-n, x+1):
                if y >= 0:
                    list_previous_word.append(sentence[y])

            # Populate the pred_dict with each different n
            for i in range(0, len(list_previous_word)-1):
                populate_pred_dict(list_previous_word[i:], pred_dict)

    return pred_dict


def populate_pred_dict(list_word, pred_dict):

    # Creating dict to search in the recursive structure
    current_dict = pred_dict

    # We search the phrase trought the dictionary and stop before the last word
    for x in range(0, len(list_word)-1):
        if list_word[x] in current_dict:
            current_dict = current_dict[list_word[x]]['next']
        else:
            current_dict[list_word[x]] = dict()
            current_dict[list_word[x]]['score'] = 0
            current_dict[list_word[x]]['next'] = dict()

            current_dict = current_dict[list_word[x]]['next']

    # Here we increment the occurence for the last word in the last dict
    if list_word[len(list_word)-1] in current_dict:
        current_dict[list_word[len(list_word)-1]]['score'] += 1
    else:
        current_dict[list_word[len(list_word)-1]] = dict()
        current_dict[list_word[len(list_word)-1]]['score'] = 1
        current_dict[list_word[len(list_word)-1]]['next'] = dict()


def predict_with_laplace(prediction_dictionnary, previous_words, lookedup_word):
    current_dict = prediction_dictionnary
    for p_word in previous_words:
        if p_word in current_dict:
            current_dict = current_dict[p_word]['next']
        else:
            return 1/len(prediction_dictionnary)

    ch = 0
    for key, value in current_dict.items():
        ch += value['score']

    if lookedup_word in current_dict:
        return ((current_dict[lookedup_word]['score'] + 1)
                / (ch+len(prediction_dictionnary)))
    else:
        return 1/(ch+len(prediction_dictionnary))


def predict_with_linear_interpolation(pred_dict, previous_word, lookedup_word, lambda_list):
    total_proba = 0

    for x in range(0, len(lambda_list)):
        current_previous_word = previous_word[x:]
        prob = get_proba(pred_dict, current_previous_word, lookedup_word)
        print(prob)
        total_proba += lambda_list[x] * prob

    return total_proba


def get_proba(pred_dict, previous_word, lookedup_word):
    current_dict = pred_dict

    for p_word in previous_word:

        if p_word in current_dict:
            current_dict = current_dict[p_word]['next']
        else:
            return 0

    ch = 0
    for key, value in current_dict.items():
        ch += value['score']

    if lookedup_word in current_dict:
        return current_dict[lookedup_word]['score']/ch
    else:
        return 0
"""
def estimation_maximisation(sentence_array, n):
    lambda_list = [1/n] * n

    for x in range(20, 40):
        sentence_train = sentence_array[:(x)] + sentence_array[(x+1):]
        sentence_test = sentence_array[x]

        pred_dict = prediction_dictionnary(sentence_train, 5)

        for lambd in range(0, len(lambda_list)):
            expectation = compute_expectation(pred_dict, lambd, lambda_list, sentence_test)
            lambda_list[lambd] = expectation/len(sentence_array)

    return lambda_list



def compute_expectation(pred_dict, lamdb, lambda_list, sentence_test):
    total = 0
    for x in range(lamdb+1, len(sentence_test)):
        prev_word = sentence_test[(x-lamdb+1):x]
        lookedup_word = sentence_test[x]
        numerator += lambda_list[lamdb] * get_proba(pred_dict, prev_word, lookedup_word)
        denominator = 0
        for y in range(0, len(lambda_list)):
            if(x-y+1) >= 0:
                prev_word = sentence_test[(x-y+1):x]
                lookedup_word = sentence_test[x]
                denominator += lambda_list[y] * get_proba(pred_dict,
                                                          prev_word,
                                                          lookedup_word)

        total += numerator/denominator
"""


def compute_perplexity_laplace(pred_dict, sentence_array, n):
    m = 0
    total_perplexity = 0
    out_of_vocab = 0

    current_sentence = 0
    print(len(sentence_array))
    for sentence in sentence_array:
        print(total_perplexity)
        print(out_of_vocab)
        print(m)
        current_sentence += 1
        print(str(current_sentence) + "/" + str(len(sentence_array)))
        for wordIndex in range(n, len(sentence)):
            if sentence[wordIndex] == '<UNK>':
                out_of_vocab += 1
            m += 1
            previous_word_array = list()
            for previous_word_index in range(wordIndex-n, n):
                previous_word_array.append(sentence[previous_word_index])
            proba = predict_with_laplace(pred_dict,
                                         previous_word_array,
                                         sentence[wordIndex])
            total_perplexity += math.log(proba, 2)

    return 2**(-1*(total_perplexity/m)), out_of_vocab/m
