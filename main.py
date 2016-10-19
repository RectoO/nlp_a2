from text_to_corpus import get_words_array


if __name__ == '__main__':
    path = "Dumas/Dumas_train.txt"
    word_array = get_words_array(path)

    print(len(word_array))
