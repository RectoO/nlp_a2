from pre_process import pre_process, get_sentences, sentence_array
from printer import print_all_n_gram, print_all_perplexity
from prediction_dictionary import prediction_dictionary
from discounting_factor import discounting_factor
from prediction import proba_laplace, proba_backoff_smoothing
import math


class Predictor(object):
    """
    TODO
    """
    def __init__(self, train_path, test_path):
        # Preprocessed train and test
        self.processed_train = pre_process(train_path)
        self.processed_test = pre_process(test_path)

        # Sentence array without unknown
        self.train_array_no_unk = sentence_array(self.processed_train)
        # Sentence array without occ -3
        train, test = get_sentences(self.processed_train, self.processed_test)
        self.train_array = train
        self.test_array = test

    def print_n_gram_info(self, n=4, array='train'):
        if array == 'train':
            print_all_n_gram(self.train_array, n)
        elif array == 'test':
            print_all_n_gram(self.train_array, n)
        else:
            print("Array not found")

    def print_perplexity(self, method, n, array):
        perplexities = []
        for x in range(1, n + 1):
            print("Computing perplexities for n = " + str(x))
            pp, oov = self.calculate_perplexity(method, x, array=array)
            result = {
                'n': x,
                'perplexity': pp,
                'oov_rate': oov
            }
            perplexities.append(result)
        print_all_perplexity(array, perplexities, method, array)

    def build_prediction_dictionary(self, n=3):
        self.pred_dict = prediction_dictionary(self.train_array, n)

    def build_discounting_factor(self, n=5):
        self.dc_array = discounting_factor(self.train_array_no_unk,
                                           self.train_array,
                                           n)

    def proba(self, previous_word, word, method):
        if method == 'laplace':
            return proba_laplace(self.pred_dict, previous_word, word)
        elif method == 'backoff':
            n = len(previous_word) + 1
            return proba_backoff_smoothing(self.pred_dict,
                                           previous_word,
                                           word,
                                           n,
                                           self.dc_array)
        else:
            print("Method : " + str(method) + " not recognized")

    def check_consistency(self, previous_word, method):
        total_proba = 0
        for key, value in self.pred_dict.items():
            total_proba += self.proba(previous_word, key, method)

        return total_proba

    def calculate_perplexity(self, method, n, array='test'):
        sentence_array = list()
        if array == 'test':
            sentence_array = self.test_array
        elif array == 'train':
            sentence_array = self.train_array
        else:
            print("Array : " + str(array) + " not recognized")
            return

        # The amout of time we computed a proba
        m = 0

        # The total current preplexity
        total_perplexity = 0

        # Number of out of vocab words
        out_of_vocab = 0

        current_sentence = 0
        print(len(sentence_array))
        # For each sentence in the sentence set
        for sentence in sentence_array:
            current_sentence += 1
            if current_sentence % 100 == 0:
                print(str(current_sentence) + "/" + str(len(sentence_array)))

            # For each word in the sentence we compute the perplexity
            # We start at n becasue we can' estimate words earlier than n
            # because we don't have enought history
            for wordIndex in range(n-1, len(sentence)):
                # Here verify that the word in not out of vocab
                if sentence[wordIndex] == '<UNK>':
                    out_of_vocab += 1

                m += 1

                # We compute with laplace the proba of this event
                proba = self.proba(sentence[wordIndex-(n-1):wordIndex],
                                   sentence[wordIndex],
                                   method)

                # We add the log of this proba to the total perplexity
                total_perplexity += math.log(proba, 2)

        print(str(current_sentence) + "/" + str(len(sentence_array)))
        return 2**(-1*(total_perplexity/m)), out_of_vocab/m
