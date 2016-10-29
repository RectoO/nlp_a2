from backoff_smoothing import proba_backoff_smoothing

def check_consistency(prediction_dictionnary, previous_words):
    current_dict = prediction_dictionnary
    total_proba = 0

    # We search in the dictionnary to the point where
    # we want to compute the check_consistency
    for p_word in previous_words:
        if p_word in current_dict:
            current_dict = current_dict[p_word]['next']
        else:
            for key, value in prediction_dictionnary.items():
                total_proba += 1/(len(prediction_dictionnary))

            return total_proba

    # We get the amount of time the previous_word where found
    ch = 0
    for key, value in current_dict.items():
        ch += value['score']

    # We compute the consistence in total_proba
    for key, value in prediction_dictionnary.items():
        if key in current_dict:
            total_proba += ((current_dict[key]['score'] + 1) /
                            (ch+len(prediction_dictionnary)))
        else:
            total_proba += 1/(ch+len(prediction_dictionnary))

    return total_proba


def check_consistency_backoff(pred_dict, ngram_occ_dict, previous_words, n):
    total_proba = 0
    i = 0
    for key, value in pred_dict.items():
        i += 1
        print(str(i) + " / " + str(len(pred_dict.keys())))
        #print(key)
        total_proba += proba_backoff_smoothing(pred_dict,
                                               previous_words,
                                               key,
                                               n,
                                               ngram_occ_dict)

    return total_proba
