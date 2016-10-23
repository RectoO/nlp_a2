from printer import plot_ngram, plot_ngram_list
from text_to_corpus import get_sentence_array_process
from n_gram import n_gram, ngram_occurence


if __name__ == '__main__':
    train_path = "Dumas/Dumas_train.txt"
    print("Preprocessing input : "+train_path)
    # Transform the text into sentence array
    train_word_array = get_sentence_array_process(train_path)
    # Data of our n_gram frequency of frequency
    n_gram_dict_list = []
    color_list = ["purple", "blue", "red"]
    gram_list = []

    # Building n_gram and plot
    for n in range(1, 4):
        # n_gram
        gram = 4-n
        print("Building "+str(gram)+"_gram histogram")
        # Buid the n_gram dict
        n_gram_dict = n_gram(train_word_array, gram)
        # Build the frequency of frequency
        occurence_dict = ngram_occurence(n_gram_dict)
        # Plot the histogram
        plot_ngram(occurence_dict, gram, color_list[n-1])
        # Add the result to our data of n_gram
        n_gram_dict_list.append(occurence_dict)
        gram_list.append(gram)

    # Plot all the n_gram together
    plot_ngram_list(n_gram_dict_list, gram_list, color_list)
    print("All histograms printed")
