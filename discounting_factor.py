from n_gram import n_gram, ngram_occurence


def discounting_factor(train_array_no_unk, train_array, n):
    # Building the ngram occurence dictionary
    ngram_occ_dict = dict()
    n_gram_dict = n_gram(train_array_no_unk, 1)
    ngram_occ = ngram_occurence(n_gram_dict)
    ngram_occ_dict["1"] = ngram_occ
    for x in range(2, n + 1):
        n_gram_dict = n_gram(train_array, x)
        ngram_occ = ngram_occurence(n_gram_dict)
        ngram_occ_dict[str(x)] = ngram_occ

    # Calculating the discounting factor
    for x in range(0, n):
        pass

    # Return the discounting factors
    return
