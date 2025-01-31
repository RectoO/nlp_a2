from predictor import Predictor

if __name__ == '__main__':
    train_path = "Dumas/Dumas_train.txt"
    test_path = "Dumas/Dumas_test.txt"

    # Init predictor
    print("Initializing the predictor...")
    my_predictor = Predictor(train_path, test_path)

    # Printing info
    """
    print("Printing n_gram info...")
    my_predictor.print_n_gram_info(n=4, array='train')
    """

    # Building the prediction dictionary
    print("Building the prediction dictionary...")
    my_predictor.build_prediction_dictionary(n=5)

    # Building the ngram occurence dictionary
    print("Building the discounting factors...")
    my_predictor.build_discounting_factor(n=5)

    print("Computing the perplexity for laplace on test...")
    my_predictor.print_perplexity('laplace', 5, 'test')

    print("Computing the perplexity for backoff on test...")
    my_predictor.print_perplexity('backoff', 5, 'test')

    print("Computing the perplexity for laplace on train...")
    my_predictor.print_perplexity('laplace', 5, 'train')

    print("Computing the perplexity for backoff on train...")
    my_predictor.print_perplexity('backoff', 5, 'train')
