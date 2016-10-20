def check_consistency(prediction_dictionnary, previous_words):
    current_dict = prediction_dictionnary
    total_proba = 0

    for p_word in previous_words:
        if p_word in current_dict:
            current_dict = current_dict[p_word]
        else:
            for key, value in prediction_dictionnary.items():
                total_proba += 1/(len(prediction_dictionnary))

            return total_proba
    ch = 0
    for key, value in current_dict.items():
        ch += value
    print("Number of word: "+str(len(prediction_dictionnary)))
    for key, value in prediction_dictionnary.items():
        if key in current_dict:
            total_proba += ((current_dict[key] + 1) /
                            (ch+len(prediction_dictionnary)))
        else:
            total_proba += 1/(ch+len(prediction_dictionnary))

    return total_proba
