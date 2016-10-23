def n_gram(sentence_list, n):
    n_gram_dict = dict()
    for sentence in sentence_list:
        for wordIndex in range(0, len(sentence)-(n-1)):
            word = list()
            for x in range(0, n):
                word.append(sentence[(wordIndex + x)])

            wordHash = str(word)
            if wordHash in n_gram_dict:
                n_gram_dict[wordHash] += 1
            else:
                n_gram_dict[wordHash] = 1

    return n_gram_dict


def ngram_occurence(ngram_dict):
    occurence_dict = dict()
    for key, value in ngram_dict.items():
        if value in occurence_dict:
            occurence_dict[value] += 1
        else:
            occurence_dict[value] = 1

    return occurence_dict
