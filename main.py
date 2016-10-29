from text_to_corpus import (get_words_array,
                            pre_process,
                            prediction_dictionnary,
                            predict_with_laplace,
                            get_sentence_array,
                            predict_with_linear_interpolation,
                            compute_perplexity_laplace,
                            sentence_array)
from n_gram import (n_gram,
                    ngram_occurence
                    )

from backoff_smoothing import proba_backoff_smoothing

from printer import print_occurence, print_ngram, print_ngram_occ
from checker import check_consistency, check_consistency_backoff
import json

if __name__ == '__main__':
    train_path = "Dumas/Dumas_train.txt"
    test_path = "Dumas/Dumas_test.txt"
    train_sentence_array, test_sentence_array = get_sentence_array(train_path,
                                                                   test_path)

    no_unk_sentence_array = sentence_array(pre_process(train_path))

    n_gram_dict1 = n_gram(no_unk_sentence_array, 1)
    n_gram_dict2 = n_gram(no_unk_sentence_array, 2)
    n_gram_dict3 = n_gram(no_unk_sentence_array, 3)
    n_gram_dict4 = n_gram(no_unk_sentence_array, 4)
    n_gram_dict5 = n_gram(no_unk_sentence_array, 5)
    """
    print_ngram(n_gram_dict1, './ngram/ngram1')
    print_ngram(n_gram_dict2, './ngram/ngram2')
    print_ngram(n_gram_dict3, './ngram/ngram3')
    print_ngram(n_gram_dict4, './ngram/ngram4')
    """
    ngram_occ1 = ngram_occurence(n_gram_dict1)
    ngram_occ2 = ngram_occurence(n_gram_dict2)
    ngram_occ3 = ngram_occurence(n_gram_dict3)
    ngram_occ4 = ngram_occurence(n_gram_dict4)
    ngram_occ5 = ngram_occurence(n_gram_dict5)

    ngram_occ_dict = {
                "1": ngram_occ1,
                "2": ngram_occ2,
                "3": ngram_occ3,
                "4": ngram_occ4,
                "5": ngram_occ5
                }
    """
    print_ngram_occ(ngram_occ1, "./ngramtest/ngramocc1")
    print_ngram_occ(ngram_occ2, "./ngramtest/ngramocc2")
    print_ngram_occ(ngram_occ3, "./ngramtest/ngramocc3")
    print_ngram_occ(ngram_occ4, "./ngramtest/ngramocc4")
    """

    print("Creating dictionnary...")
    pred_dict = prediction_dictionnary(train_sentence_array, 5)
    #print('<s>' in pred_dict)
    #print("Computing perplexity")
    #print(compute_perplexity_laplace(pred_dict, test_sentence_array, 1))


    #print(proba_backoff_smoothing(pred_dict, ['<s>', 'it'], 'is', 2, ngram_occ_dict))



    #print("Done creating dictionnary...")

    #print(json.dumps(pred_dict, indent=2))
    #print(json.dumps(pred_dict['indeed']['next']['you']['next']['are']['next']['right'], indent=2))
    #print(check_consistency(pred_dict, ['indeed', 'you', 'are', 'right']))

    #print(predict_with_linear_interpolation(pred_dict, ['<s>', 'what', 'do'], 'you', [0.33, 0.33, 0.33]))
