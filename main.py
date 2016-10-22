from text_to_corpus import (get_words_array,
                            pre_process,
                            n_gram,
                            ngram_occurence,
                            prediction_dictionnary,
                            predict_with_laplace,
                            get_sentence_array)
from printer import print_occurence, print_ngram, print_ngram_occ
from checker import check_consistency
import json

if __name__ == '__main__':
    train_path = "Dumas/Dumas_train.txt"
    test_path = "Dumas/Dumas_test.txt"
    train_word_array = get_sentence_array(train_path)
    with open("output.txt", 'w', encoding='utf-8') as output:
        for sentence in train_word_array:
            output.write(str(sentence)+'\n')
    # test_word_array = pre_process(test_path)

    # print_occurence(word_array, "word_occurence.txt")
    """
    n_gram_dict1 = n_gram(train_word_array, 1)
    n_gram_dict2 = n_gram(train_word_array, 2)
    n_gram_dict3 = n_gram(train_word_array, 3)
    n_gram_dict4 = n_gram(train_word_array, 4)

    print_ngram(n_gram_dict1, './ngram/ngram1')
    print_ngram(n_gram_dict2, './ngram/ngram2')
    print_ngram(n_gram_dict3, './ngram/ngram3')
    print_ngram(n_gram_dict4, './ngram/ngram4')

    ngram_occ1 = ngram_occurence(n_gram_dict1)
    ngram_occ2 = ngram_occurence(n_gram_dict2)
    ngram_occ3 = ngram_occurence(n_gram_dict3)
    ngram_occ4 = ngram_occurence(n_gram_dict4)

    print_ngram_occ(ngram_occ1, "./ngramocc/ngramocc1")
    print_ngram_occ(ngram_occ2, "./ngramocc/ngramocc2")
    print_ngram_occ(ngram_occ3, "./ngramocc/ngramocc3")
    print_ngram_occ(ngram_occ4, "./ngramocc/ngramocc4")
    pred_dict = prediction_dictionnary(train_word_array, 2)
    # print(pred_dict['of']['the'])
    print(check_consistency(pred_dict, ['i', 'aaa']))
    """
    print("Creating dictionnary...")
    pred_dict = prediction_dictionnary(train_word_array, 5)
    #print("Done creating dictionnary...")

    #print(json.dumps(pred_dict, indent=2))
    print(json.dumps(pred_dict['indeed']['next']['you']['next']['are']['next']['right'], indent=2))
    #print(check_consistency(pred_dict, ['indeed', 'you', 'are', 'right']))
