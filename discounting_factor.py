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
    discounting_array = list()

    for x in range(0, n):
        n1 = ngram_occ_dict[str(x+1)][1]
        n2 = ngram_occ_dict[str(x+1)][2]

        discounting_array.append((n1 / (n1 + (2*n2))))
    print(discounting_array)
    # Return the discounting factors
    return discounting_array
