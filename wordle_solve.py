from pathlib import Path
import string
from matplotlib import markers, pyplot as plt

answers_list = Path('answers.txt').read_text().splitlines()
guesses_list = Path('guesses.txt').read_text().splitlines()
combined_list = Path('combined.txt').read_text().splitlines()
alphabet_list = string.ascii_uppercase

class WordList:
    """Just an abstraction so I don't have to pass lists around."""
    def __init__(self, answer_list, guess_list):
        """I'm not giving it a default list, so you'll need to put in your lists."""
        self.answer_list = answer_list
        self.guess_list  = guess_list

    def search_right_letter_right_position( self, letter, position ):
        new_answers = []
        new_guesses = []
        for word in self.answer_list:
            if word[position] == letter:
                new_answers.append(word)
        
        self.answer_list = new_answers

        for word in self.guess_list:
            if word[position] == letter:
                new_guesses.append(word)

        self.guess_list = new_guesses

    def search_right_letter_wrong_position(self, letter, position):
        new_answers = []
        new_guesses = []

        for word in self.answer_list:
            if letter in word and word[position] != letter:
                new_answers.append(word)

        self.answer_list = new_answers

        for word in self.guess_list:
            if letter in word and word[position] != letter:
                new_guesses.append(word)

        self.guess_list = new_guesses

    def search_wrong_letter_wrong_position(self, letter ):
        new_answers = []
        new_guesses = []

        for word in self.answer_list:
            if letter not in word:
                new_answers.append(word)

        self.answer_list = new_answers

        for word in self.guess_list:
            if letter not in word:
                new_guesses.append(word)

        self.guess_list = new_guesses

    def search_letter( self, letter ):
        new_answers = []
        new_guesses = []
        
        for word in self.answer_list:
            if letter in word:
                new_answers.append(word)
        self.answer_list = new_answers

        for word in self.guess_list:
            if letter in word:
                new_guesses.append(word)
        self.guess_list = new_guesses

    def print_answers(self):
        print(self.answer_list)

    def print_guesses(self):
        print(self.guess_list)

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

def guess_list_stats():
    one_letter = [0 for i in range(26)]
    two_letter = [0 for i in range(26)]
    three_letter = [0 for i in range(26)]

    for letter in alphabet_list:
        for word in guesses_list:
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
    plt.title('At Least One Occurrence of Letter in Guess Words')
    plt.ylabel('Occurrences')
    plt.show()

    # Two letter
    plt.bar( x_labels, two_letter )
    plt.title('At Least Two Occurrences of Letter in Guess Words')
    plt.ylabel('Occurences')
    plt.show()

    # Three letter
    plt.bar( x_labels, three_letter )
    plt.title('At Least Three Occurrences of Letter in Guess Words')
    plt.ylabel('Occurrences')
    plt.show()

if __name__ == '__main__':
    my_list = WordList(answers_list,guesses_list)
    my_list.search_letter('E')
    my_list.search_letter('R')
    my_list.search_letter('A')
    my_list.search_letter('T')
    my_list.search_letter('C')
    answers_list = my_list.answer_list
    answer_list_stats()
    my_list.print_answers()