def proba_backoff_smoothing(pred_dict,
                            previous_words,
                            lookedup_word,
                            n,
                            n1,
                            n2):

    # Init some usefull variables for further compute_expectation
    count_h_w = 0
    count_h = 0
    occurence = True

    # Creaing dictionary to naviguate in the pred_dict
    current_dict = pred_dict()

    # Length of history
    p_length = len(previous_words)

    # Naviguating in the pre_dict
    for x in range(0, n):
        key = previous_words[p_length-n+x]
        if key in current_dict.items():
            current_dict = current_dict[key]['next']
        else:
            no_occurence = False

    # Now that we are in the right dictionnary we compute count_h_w and count_h
    if occurence:

        # We count count_h
        for key, value in current_dict.items():
            count_h += value['score']

        # We get count_h_w
        if lookedup_word in current_dict:
            count_h_w = current_dict[lookedup_word]['score']

    # Frist case if count_h equal 0 for the backoff_smoothing
    if count_h == 0:
        # We can't evaluate a model for n < 0
        if n == 0:
            return 0
        # Else we compute the P_back proba
        else:
            return proba_backoff_smoothing(pred_dict,
                                           previous_words,
                                           lookedup_word,
                                           n-1)

    # For the two others cases of backoff smoothing we need to compute y_h and d_c
    y_h = 0
    d_c =
