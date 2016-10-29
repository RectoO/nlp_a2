def prediction_dictionary(sentence_list, n):
    pred_dict = dict()
    # We built the dictionnary for each sentence
    for sentence in sentence_list:
        # We iterate trought the words of the sentence
        for x in range(0, len(sentence)):
            # We create a list of the previous word for the current word
            previous_word = list()
            for y in range(x-(n+1), x):
                if y >= 0:
                    previous_word.append(sentence[y])

            # Populate the pred_dict with each different n
            for i in range(0, len(previous_word)+1):
                populate_pred_dict(previous_word[i:], sentence[x], pred_dict)

    return pred_dict


def populate_pred_dict(prev_word, current_word, pred_dict):

    # Creating dict to search in the recursive structure
    current_dict = pred_dict

    # We search the phrase trought the dictionary and stop before the last word
    for x in range(0, len(prev_word)):
        if prev_word[x] in current_dict:
            current_dict = current_dict[prev_word[x]]['next']
        else:
            current_dict[prev_word[x]] = dict()
            current_dict[prev_word[x]]['score'] = 0
            current_dict[prev_word[x]]['next'] = dict()

            current_dict = current_dict[prev_word[x]]['next']

    # Here we increment the occurence for the last word in the last dict
    if current_word in current_dict:
        current_dict[current_word]['score'] += 1
    else:
        current_dict[current_word] = dict()
        current_dict[current_word]['score'] = 1
        current_dict[current_word]['next'] = dict()
