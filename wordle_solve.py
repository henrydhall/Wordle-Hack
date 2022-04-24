# Libraries I need.
from pathlib import Path
import string
from matplotlib import markers, pyplot as plt

# Globals I need.
answers_list = Path('answers.txt').read_text().splitlines()
guesses_list = Path('guesses.txt').read_text().splitlines()
combined_list = Path('combined.txt').read_text().splitlines()
alphabet_list = string.ascii_uppercase
WORD_LENGTH = 5

class WordList:
    """
    Just an abstraction so I don't have to pass lists around.
    """
    def __init__(self, answer_list, guess_list):
        """
        I'm not giving it a default list, so you'll need to put in your lists.
        """
        self.answer_list = answer_list
        self.guess_list  = guess_list
        self.narrowed_answer_list = answer_list
        self.narrowed_guess_list = guess_list
        self.found_letters = set()         # For holding the SET of found letters.
        self.eliminated_letters = set()    # For holding the SET of eliminated letters.

    def search_right_letter_right_position( self, letter, position ):
        """
        Use to keep words with the letter given in the position given.
        Parameters- letter: the letter to keep. position: the position (0-4) the letter is in.
        Returns- none. Does set the answer_list to the new list.
        """
        self.found_letters.add(letter)
        new_answers = []
        new_guesses = []
        for word in self.narrowed_answer_list:
            if word[position] == letter:
                new_answers.append(word)
        
        self.narrowed_answer_list = new_answers

        for word in self.narrowed_guess_list:
            if word[position] == letter:
                new_guesses.append(word)

        self.narrowed_guess_list = new_guesses

    def search_right_letter_wrong_position(self, letter, position):
        """
        Use to keep words with the letter in any position but the one given.
        Parameters- letter: the letter to keep. position: the position (0-4) the letter is not in.
        Returns- none. Does set the answer_list to the new list.
        """
        self.found_letters.add(letter)
        new_answers = []
        new_guesses = []

        for word in self.narrowed_answer_list:
            if letter in word and word[position] != letter:
                new_answers.append(word)

        self.narrowed_answer_list = new_answers

        for word in self.narrowed_guess_list:
            if letter in word and word[position] != letter:
                new_guesses.append(word)

        self.narrowed_guess_list = new_guesses

    def search_wrong_letter_wrong_position(self, letter ):
        """
        Use to keep words with the letter given in the position given.
        Parameters- letter: the letter to get rid of. 
        Returns- none. Does set the answer_list to the new list.
        """
        self.eliminated_letters.add(letter)

        new_answers = []
        new_guesses = []

        for word in self.narrowed_answer_list:
            if letter not in word:
                new_answers.append(word)

        self.narrowed_answer_list = new_answers

        for word in self.narrowed_guess_list:
            if letter not in word:
                new_guesses.append(word)

        self.narrowed_guess_list = new_guesses

    def search_letter( self, letter ):
        """
        Use to only keep words with the letter in any position.
        Parameters- letter: the letter to keep.
        Returns- none. Does set the answer_list to the new list.
        """
        new_answers = []
        new_guesses = []
        
        for word in self.narrowed_answer_list:
            if letter in word:
                new_answers.append(word)
        self.narrowed_answer_list = new_answers

        for word in self.narrowed_guess_list:
            if letter in word:
                new_guesses.append(word)
        self.narrowed_guess_list = new_guesses

    def print_answers(self):
        """
        This should be clear.
        """
        print(self.answer_list)

    def print_guesses(self):
        """
        This should be clear.
        """
        print(self.guess_list)

    def print_narrowed_answers(self):
        """
        Clear
        """
        print(self.narrowed_answer_list)

    def print_narrowed_guesses(self):
        """
        Clear
        """
        print(self.narrowed_guess_list)

    def most_common_letters(self, display = False):
        """
        Finds the most common remaining letters in narrowed_answer_list, that haven't been found.
        Parameters- display: if True, display graphs of the data.
        Returns- 
            most_common_letters: the list of most common letters. If the number of occurences is equal they're in alphabetical order.
            no_occurences: True if the most frequent doesn't actually occur, False if it does.
        """
        one_letter = [0 for i in range(26)]
        two_letter = [0 for i in range(26)]
        three_letter = [0 for i in range(26)]

        most_common_letters = []
        no_occurrences = False

        for letter in alphabet_list:
            for word in self.narrowed_answer_list:
                if word.count(letter) > 2:
                    three_letter[ alphabet_list.index(letter) ] += 1
                elif word.count(letter) > 1:
                    two_letter[ alphabet_list.index(letter) ] += 1
                elif word.count(letter) > 0:
                    one_letter[ alphabet_list.index(letter) ] += 1

        for letter in self.found_letters:
            one_letter[ alphabet_list.index(letter) ] = 0 # We need to set these to 0 so we only look at letters we don't know about yet.

        if display: # This displays the bar graphs letter frequency of narrowed lists.
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

        while len( most_common_letters ) < WORD_LENGTH : # We want 5 if we can get them.
            max_frequency = max(one_letter)
            if max_frequency == 0:
                return most_common_letters
            
            for i in range(26):
                if one_letter[i] == max_frequency:
                    one_letter[i] = 0
                    most_common_letters.append( alphabet_list[i] )

        #TODO: Account for words that have other most common letters in them. (use temp WordList)

        return most_common_letters

    def play_loop(self):
        print('TODO: play_loop')

def answer_list_stats():
    """
    Process the answers_list and display stats for frequency of letters.
    """
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
    """
    Process the guesses_list and display stats for frequency of letters.
    """
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

    print( my_list.most_common_letters() )

    my_list.search_wrong_letter_wrong_position('R')
    my_list.search_wrong_letter_wrong_position('E')
    my_list.search_right_letter_right_position('A',2)
    my_list.search_wrong_letter_wrong_position('C')
    my_list.search_right_letter_right_position('T',4)

    my_list.search_right_letter_wrong_position('L',3)

    answers_list = my_list.answer_list
    my_list.print_narrowed_answers()
    print(f'Found:      {my_list.found_letters}')
    print(f'Eliminated: {my_list.eliminated_letters}')
    print( my_list.most_common_letters(True) )