import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from n_gram import n_gram, ngram_occurence


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
            percent = round(value/1398349.0, 3)
            output.write(key+" = "+str(value)+" ("+str(percent)+"%)\n")


def print_all_n_gram(array, n):
    color_list = ["purple", "blue", "red", "yellow"]
    for x in range(1, n + 1):
        print(str(x) + "-gram...")
        n_gram_dict = n_gram(array, x)
        print_ngram(n_gram_dict, './ngram/ngram' + str(x))
        ngram_occ = ngram_occurence(n_gram_dict)
        print_ngram_occ(ngram_occ, './ngramocc/ngramocc' + str(x))
        plot_ngram(ngram_occ, x, color_list[x-1])


def print_ngram(ngram_dict, path):

    with open(path, 'w', encoding="utf-8") as output:
        occurence_list = []
        total_word = 0
        for key, value in ngram_dict.items():
            total_word += value
            occurence_list.append((key, value))
        output.write("Total : " + str(total_word) + "\n")
        output.write("Differents : " + str(len(ngram_dict)) + "\n")
        for (key, value) in sorted(occurence_list,
                                   key=lambda x: (-x[1], x[0])):
            percent = round((value/total_word) * 100, 3)
            output.write(key+" = "+str(value)+" ("+str(percent)+"%)\n")


def print_ngram_occ(ngram_dict, path):

    with open(path, 'w', encoding="utf-8") as output:
        occurence_list = []
        for key, value in ngram_dict.items():
            occurence_list.append((key, value))
        for (key, value) in sorted(occurence_list,
                                   key=lambda x: (-x[1], x[0])):
            output.write(str(key)+" = "+str(value)+"\n")


def plot_ngram(ngram_dict, gram, color="purple"):
    # The Data
    occurence_list, x, y = [], [], []
    for key, value in ngram_dict.items():
        occurence_list.append((key, value))
    for (key, value) in sorted(occurence_list,
                               key=lambda x: (-x[1], x[0])):
        x.append(key)
        y.append(value)

    # The plot
    plt.figure()
    plt.bar(x, y, color="white", edgecolor=color, align="center", log=True)
    plt.xscale('log')
    plt.xlim(xmin=0)

    # The legend
    patch = mpatches.Patch(color=color, label=str(gram)+'-gram')
    plt.legend(handles=[patch])

    # Save the plot
    file_path = "n_gram_plot/"+str(gram)+"_gram_count_histogram.png"
    plt.savefig(file_path)
    plt.close()


def plot_ngram_list(ngram_dict_list, gram_list, color_list):
    # The data
    x_list, y_list = [], []
    for ngram_dict in ngram_dict_list:
        occurence_list, x, y = [], [], []
        for key, value in ngram_dict.items():
            occurence_list.append((key, value))
        for (key, value) in sorted(occurence_list,
                                   key=lambda x: (-x[1], x[0])):
            x.append(key)
            y.append(value)
        x_list.append(x)
        y_list.append(y)

    # The plot
    patch_list = []
    plt.figure()
    for x, y, g, c in zip(x_list, y_list, gram_list, color_list):
        # Bar plot
        plt.bar(x, y, color="white", edgecolor=c, align="center", log=True)
        # Legend
        patch = mpatches.Patch(color=c, label=str(g)+'-gram')
        patch_list.append(patch)
    plt.legend(handles=patch_list)
    plt.xscale('log')
    plt.xlim(xmin=0)

    # Save the plot
    file_path = "n_gram_plot/all_gram_count_histogram.png"
    plt.savefig(file_path)
    plt.close()
