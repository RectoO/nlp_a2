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
            output.write(key+" = "+str(value)+" ("+str(round(value/1398349.0,3))+"%)\n")


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
