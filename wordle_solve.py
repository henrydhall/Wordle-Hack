from pathlib import Path
import string
from matplotlib import markers, pyplot as plt

answers_list = Path('answers.txt').read_text().splitlines()
guesses_list = Path('guesses.txt').read_text().splitlines()
combined_list = Path('combined.txt').read_text().splitlines()
alphabet_list = string.ascii_uppercase

def answer_list_stats():
    one_letter = [0 for i in range(26)]
    two_letter = [0 for i in range(26)]
    three_letter = [0 for i in range(26)]
    for letter in alphabet_list:
        for word in answers_list:
            if word.count(letter) > 2:
                three_letter[ alphabet_list.index(letter) ] += 1
            elif word.count(letter) > 1:
                two_letter[ alphabet_list.index(letter) ] += 1
            elif word.count(letter) > 0:
                one_letter[ alphabet_list.index(letter) ] += 1

    # Make x labels for the bar graph
    x_labels = [letter for letter in alphabet_list]

    # One letter
    plt.bar( x_labels, one_letter )
    plt.title('At Least One Occurrence of Letter in Answer Words')
    plt.ylabel('Occurrences')
    plt.show()

    # Two letter
    plt.bar( x_labels, two_letter )
    plt.title('At Least Two Occurrences of Letter in Answer Words')
    plt.ylabel('Occurences')
    plt.show()

    # Three letter
    plt.bar( x_labels, three_letter )
    plt.title('At Least Three Occurrences of Letter in Answer Words')
    plt.ylabel('Occurrences')
    plt.show()

if __name__ == '__main__':
    answer_list_stats()