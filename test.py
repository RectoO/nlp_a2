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

    train_word_array = get_words_array(train_path)
    print(len(train_word_array))

    print_occurence(train_word_array, "occurence.txt")
