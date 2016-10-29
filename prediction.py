def proba_laplace(pred_dict, previous_words, lookedup_word):
    current_dict = pred_dict
    for p_word in previous_words:
        if p_word in current_dict:
            current_dict = current_dict[p_word]['next']
        else:
            return 1/len(pred_dict)

    ch = 0
    for key, value in current_dict.items():
        ch += value['score']

    if lookedup_word in current_dict:
        return ((current_dict[lookedup_word]['score'] + 1)
                / (ch+len(pred_dict)))
    else:
        return 1/(ch+len(pred_dict))


def proba_backoff_smoothing(pred_dict,
                            previous_words,
                            lookedup_word,
                            n,
                            ngram_occ_dict):
    if n < 0:
        return 0
    # Init some usefull variables for further compute_expectation
    count_h_w = 0
    count_h = 0
    occurence = True

    # Creaing dictionary to naviguate in the pred_dict
    current_dict = pred_dict

    # Length of history
    p_length = len(previous_words)

    # Naviguating in the pre_dict
    for x in range(0, n):
        # print(occurence)
        key = previous_words[p_length-n+x]
        # print(key)
        if key in current_dict:
            current_dict = current_dict[key]['next']
        else:
            occurence = False

    # Now that we are in the right dictionnary we compute count_h_w and count_h
    if occurence:

        # We count count_h
        for key, value in current_dict.items():
            count_h += value['score']

        # We get count_h_w
        if lookedup_word in current_dict:
            count_h_w = current_dict[lookedup_word]['score']

    # print("count h : " + str(count_h))
    # print("count h w : " + str(count_h_w))

    d_c = 0
    y_h = 0

    # We compute y_h and d_c d_c and y_h
    if n > 0:
        n1 = ngram_occ_dict[str(n)][1]
        n2 = ngram_occ_dict[str(n)][2]
    else:
        n1 = ngram_occ_dict['1'][1]
        n2 = ngram_occ_dict['1'][2]

        d_c = n1 / (n1 + (2 * n2))
        # print("dc : " + str(d_c))
        y_h = len(current_dict.keys()) * (d_c / count_h)
        # print("yh : " + str(y_h))

    # First case of backoff smoothing
    if count_h_w > 0:
        return ((count_h_w-d_c)/count_h) + y_h*proba_backoff_smoothing(
                                        pred_dict,
                                        previous_words,
                                        lookedup_word,
                                        n-1,
                                        ngram_occ_dict)

    # Second case of backoff smoothing
    if count_h_w == 0 and count_h > 0:
        return y_h*proba_backoff_smoothing(
                                        pred_dict,
                                        previous_words,
                                        lookedup_word,
                                        n-1,
                                        ngram_occ_dict)

    # Third case of backoff smoothing
    if count_h == 0:
        # We can't evaluate a model for n < 0
        if n == 0:
            return 0
        # Else we compute the P_back proba
        else:
            return proba_backoff_smoothing(pred_dict,
                                           previous_words,
                                           lookedup_word,
                                           n-1,
                                           ngram_occ_dict)
