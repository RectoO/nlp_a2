from pre_process import pre_process, get_sentences, sentence_array
from printer import print_all_n_gram, print_all_perplexity
from prediction_dictionary import prediction_dictionary
from discounting_factor import discounting_factor
from prediction import proba_laplace, proba_backoff_smoothing


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

    def print_perplexity(self, method, array, n):
        perplexities = []
        for x in range(1, n + 1):
            pp, oov = self.calculate_perplexity(method, n, array=array)
            result = {
                'n': x,
                'perplexity': pp,
                'oov_rate': oov
            }
            perplexities.append(result)
        print_all_perplexity(array, perplexities, method)

    def build_prediction_dictionary(self, n=3):
        self.pred_dict = prediction_dictionary(self.train_array, n)

    def build_discounting_factor(self, n=5):
        self.dc_dict = discounting_factor(self.train_array_no_unk,
                                          self.train_array,
                                          n)

    def proba(self, previous_word, word, method):
        if method == 'laplace':
            return proba_laplace(self.pred_dict, previous_word, word)
        elif method == 'backoff':
            n = len(previous_word)
            return proba_backoff_smoothing(self.pred_dict,
                                           previous_word,
                                           word,
                                           n,
                                           self.dc_dict)
        else:
            print("Method : " + str(method) + " not recognized")

    def check_consistency(self, previous_word, method):
        total_proba = 0
        for key, value in self.pred_dict.items():
            total_proba += self.proba(previous_word, key, method)

        return total_proba

    def calculate_perplexity(self, method, n, array='test'):
        pass
