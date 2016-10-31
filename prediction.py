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
                            dc_array):

    # We stop the recution if n < 1
    if n < 1:
        return 0

    # Init some usefull variables for further compute_expectation
    count_h_w = 0
    count_h = 0
    occurence = True

    # Creating dictionary to naviguate in the pred_dict
    current_dict = pred_dict

    # Length of history
    p_length = len(previous_words)

    # Naviguating in the pre_dict
    for x in range(0, n-1):

        key = previous_words[(p_length+1)-n+x]

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

    d_c = dc_array[n-1]
    y_h = 0

    if count_h != 0:
        y_h = len(current_dict.keys()) * (d_c / count_h)

    # First case of backoff smoothing
    if count_h_w > 0:
        return ((count_h_w-d_c)/count_h) + y_h*proba_backoff_smoothing(
                                        pred_dict,
                                        previous_words,
                                        lookedup_word,
                                        n-1,
                                        dc_array)

    # Second case of backoff smoothing
    if count_h_w == 0 and count_h > 0:
        return y_h*proba_backoff_smoothing(
                                        pred_dict,
                                        previous_words,
                                        lookedup_word,
                                        n-1,
                                        dc_array)

    # Third case of backoff smoothing
    if count_h == 0:
        return proba_backoff_smoothing(pred_dict,
                                       previous_words,
                                       lookedup_word,
                                       n-1,
                                       dc_array)
