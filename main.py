from text_to_corpus import get_words_array


if __name__ == '__main__':
    path = "Dumas/Dumas_train.txt"
    word_array = get_words_array(path)

    word_dict = {}
    for word in word_array:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1

    with open("word_occurence.txt", 'w', encoding="utf-8") as output:
        occurence_list = []
        for key, value in word_dict.items():
            occurence_list.append((key, value))
        for (key, value) in sorted(occurence_list, key=lambda x: (-x[1], x[0])):
            output.write(key+" = "+str(value)+"\n")
