from text_to_corpus import get_words_array, pre_process, n_gram, ngram_occurence, prediction_dictionnary


def print_occurence(array, path):
    word_dict = {}
    for word in array:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1

    with open(path, 'w', encoding="utf-8") as output:
        occurence_list = []
        for key, value in word_dict.items():
            occurence_list.append((key, value))
        for (key, value) in sorted(occurence_list,
                                   key=lambda x: (-x[1], x[0])):
            output.write(key+" = "+str(value)+"\n")


def print_ngram(ngram_dict, path):

    with open(path, 'w', encoding="utf-8") as output:
        occurence_list = []
        for key, value in ngram_dict.items():
            occurence_list.append((key, value))
        for (key, value) in sorted(occurence_list,
                                   key=lambda x: (-x[1], x[0])):
            output.write(key+" = "+str(value)+"\n")

def print_ngram_occ(ngram_dict, path):

    with open(path, 'w', encoding="utf-8") as output:
        occurence_list = []
        for key, value in ngram_dict.items():
            occurence_list.append((key, value))
        for (key, value) in sorted(occurence_list,
                                   key=lambda x: (-x[1], x[0])):
            output.write(str(key)+" = "+str(value)+"\n")

if __name__ == '__main__':
    train_path = "Dumas/Dumas_train.txt"
    test_path = "Dumas/Dumas_test.txt"
    train_word_array = get_words_array(train_path)
    # test_word_array = pre_process(test_path)

    # print_occurence(word_array, "word_occurence.txt")
    """
    n_gram_dict1 = n_gram(train_word_array, 1)
    n_gram_dict2 = n_gram(train_word_array, 2)
    n_gram_dict3 = n_gram(train_word_array, 3)
    n_gram_dict4 = n_gram(train_word_array, 4)

    ngram_occ1 = ngram_occurence(n_gram_dict1)
    ngram_occ2 = ngram_occurence(n_gram_dict2)
    ngram_occ3 = ngram_occurence(n_gram_dict3)
    ngram_occ4 = ngram_occurence(n_gram_dict4)

    print_ngram_occ(ngram_occ1, "./ngramocc/ngramocc1")
    print_ngram_occ(ngram_occ2, "./ngramocc/ngramocc2")
    print_ngram_occ(ngram_occ3, "./ngramocc/ngramocc3")
    print_ngram_occ(ngram_occ4, "./ngramocc/ngramocc4")
    """
    pred_dict = prediction_dictionnary(train_word_array, 1)
    print(pred_dict['of']['the'])
