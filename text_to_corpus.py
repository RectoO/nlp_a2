import re


def get_words_array(path):
    """
    Return an array of word in path. We first prune the file to remove noises
    """
    # Removed characters
    remove_char = ['"', '\'', ',', '‚', ';', '-', '(', ')', '$', '`', '*',
                   '&gt']
    # Removed section
    remove_section = [('\[', '\]'), ('<', '>')]
    # Special rules
    remove_special = [(" &amp; ", "&"), ("!", " ! "), ("?", " ? "),
                      (".", " . ")]

    # Read the file
    with open(path, 'r') as f:
        text = f.read()

    # Remove the useless characters
    for char in remove_char:
        text = text.replace(char, "")

    # Remove the useless sections
    for (begin, end) in remove_section:
        text = re.sub("("+begin+")(.)*("+end+")", "", text)

    # Applying the special replacements rules
    for (old, new) in remove_special:
        text = text.replace(old, new)

    # Return the words of the text in array
    return re.split("\s+", text)
