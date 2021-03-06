# Libraries I need.
from pathlib import Path
from re import M
import string
from matplotlib import markers, pyplot as plt, use
import pyinputplus

# Globals I need.
answers_list = Path('answers.txt').read_text().splitlines()   # Major issues with encodings in windows... TODO: fix that.
guesses_list = Path('guesses.txt').read_text().splitlines()
combined_list = Path('combined.txt').read_text().splitlines()
alphabet_list = string.ascii_uppercase
WORD_LENGTH = 5
MAX_GUESSES = 6

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
        self.solved = False
        # If any additional property is added, make sure you add it to WordList.copy() 

    def __reset__(self):
        """
        Resets the list, as if no searches had ever been made.
        """
        self.__init__( self.answer_list, self.guess_list )

    def __soft_reset__(self):
        raise NotImplementedError('soft_reset not implemented')

    def copy(self):
        """
        Returns - copy_list, a copy of the list this function is called on. 
        """
        """
        Because of the way user implemented classes work, I have to make a copy like this,
        and then return it. Otherwise it returns a WordList with a different name, but it
        points to the list that was copied.
        I use this to search a list without ruining it.
        """
        copy_list = WordList(self.answer_list, self.guess_list)
        copy_list.narrowed_answer_list = self.narrowed_answer_list
        copy_list.narrowed_guess_list  = self.narrowed_guess_list
        copy_list.eliminated_letters = self.eliminated_letters
        copy_list.found_letters = self.found_letters
        copy_list.solved = self.solved
        return copy_list

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

    def search_wrong_letter_wrong_position(self, letter, position = None):
        """
        Use to keep words with the letter given in the position given.
        Parameters- letter: the letter to get rid of, optional position for when letter is in word. 
        Returns- none. Does set the answer_list to the new list.
        """

        new_answers = []    # Initialize these lists. These become our new shortened answer lists.
        new_guesses = []

        if letter not in self.found_letters:          # If the letter we're looking to eliminate isn't also in the word.
            if letter not in self.eliminated_letters:  # If we haven't already eliminated it add it to our set of words.
                self.eliminated_letters.add(letter)
            for word in self.narrowed_answer_list:     # Look at all remaining words.
                if letter not in word:                 # If our letter isn't in the word keep it.
                    new_answers.append(word)
            for word in self.narrowed_guess_list:
                if letter not in word:
                    new_guesses.append(word)

        elif letter in self.found_letters:          # If the letter is in the word, but doesn't occur multiple times
            for word in self.narrowed_answer_list:  # Just get rid of words with the letter in the position we've narrowed.
                if word[ position ] != letter:
                    new_answers.append(word)
            for word in self.narrowed_guess_list:   # TODO: improve searching for multiple letters. Will take some work...
                if word[ position ] != letter:
                    new_guesses.append(word)

        self.narrowed_answer_list = new_answers
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
        Clear from name.
        """
        print(self.narrowed_answer_list)

    def print_narrowed_guesses(self):
        """
        Clear from name.
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
        most_common_letters = []

        # Initialize our set of found_letters, just for this function.
        checked_letters = set()
        for letter in self.found_letters:     # Fill it with letters from our two sets of letters.
            checked_letters.add(letter)
        for letter in self.eliminated_letters:
            checked_letters.add(letter)

        copy_list = self.copy() # Copy to analyze, so we don't have to worry about messing up our actual list.
        letter_frequencies = copy_list.combined_frequency()

        for letter in checked_letters:
            letter_frequencies[ alphabet_list.index(letter) ] = 0 # We need to set these to 0 so we only look at letters we don't know about yet.

        if display: # This displays the bar graphs letter frequency of narrowed lists.
            copy_list.display_narrowed_answer_list_stats()

        while len( most_common_letters ) < WORD_LENGTH : # We want 5 if we can get them.
            max_frequency = max(letter_frequencies)
            if max_frequency == 0:
                return most_common_letters
            
            for i in range(26):
                if letter_frequencies[i] == max_frequency:
                    checked_letters.add(alphabet_list[i])
                    most_common_letters.append( alphabet_list[i] )
                    copy_list.search_letter( alphabet_list[i] )
                    letter_frequencies = copy_list.combined_frequency()
                    for letter in checked_letters:
                        letter_frequencies[ alphabet_list.index(letter) ] = 0
        return most_common_letters

    def get_best_guess(self):
        """
        Gets the ideal guess(es) based on letter frequency of remaining words.
        Returns- ideal_guesses: a list of ideal guesses.
        """
        most_common_letters = self.most_common_letters()      # Get most common letters
        copy_list = self.copy()                               # Get a copy list of self to work with
        stop_point = 5                                        # We need to know if we accidentally eliminate all letters.
        for i in range(len(most_common_letters)):             # For each most common letter.
            copy_list.search_letter( most_common_letters[i] ) # Search to narrow the letters in the copied answer list.
            if len(copy_list.narrowed_answer_list) == 0:      # If there is nothing left, set stopping point to that index.
                stop_point = i
        if stop_point != 5:             # If there was nothing left, redo up to the point before there's nothing left.
            copy_list = self.copy()
            for i in range(stop_point):
                copy_list.search_letter(most_common_letters[i])
        ideal_guesses = copy_list.narrowed_answer_list
        return ideal_guesses

    def play_loop(self):
        """
        Loop to play through guessing a word all the way through.
        Runs in console. 
        """
        number_guesses = 0
        print('Let\'s play Wordle together!')
        while  number_guesses != MAX_GUESSES:
            print(f'Turn {number_guesses+1}')
            self.play_turn()
            number_guesses += 1
            if not self.solved:
                print(f'{MAX_GUESSES-number_guesses} turns left')
            if self.solved:
                return 0

        if number_guesses == MAX_GUESSES:
            print('Dang it! We didn\'t get it :(')
            
    def play_turn(self):
        """
        Plays a full turn of Wordle. Requires the user to input the guess
            and status of each letter in correct order.
        """
        player_guess = 'NONE'
        right_letter_right_position = 'NONE'
        right_letter_wrong_position = 'NONE'
        wrong_letter = 'NONE'
        valid_guess = False
        print('Here are the best guesses to use: ' )
        print( self.get_best_guess() )
        player_guess = self.get_guess() 
        print(f'We got the guess: {player_guess}') # TODO: sure this works.
        # Start Here:
        while not valid_guess:
            right_letter_right_position = self.get_right_letter_right_position()
            if self.solved:
                return
            right_letter_wrong_position = self.get_right_letter_wrong_position()
            wrong_letter = self.get_wrong_letter_wrong_position()
            if self.check_guess(player_guess,right_letter_right_position,right_letter_wrong_position,wrong_letter):
                self.search_by_guess(right_letter_right_position,right_letter_wrong_position,wrong_letter)
                valid_guess = True
        #else:
            # Change this, so that it repeats the above
        #    raise ValueError('You did not enter appropriate correctness statuses for letters')

    def get_guess(self):
        """
        Gets the guess the player made. Verifies length and if it's a legit guess.
        """
        user_input = 'NONE'
        while user_input == 'NONE':

            user_input = input('Your guess: ').upper()

            if user_input == 'H':
                print('Enter \"Print All\" to see all remaining answers.')
            elif user_input == 'PRINT ALL':
                self.print_narrowed_answers()

            if len(user_input) != 5:
                user_input = 'NONE'
                print('Guess must be 5 letters')

            if not ( user_input in self.answer_list or user_input in self.guess_list):
                user_input = 'NONE'
                print('Guess not valid.')

            for letter in user_input:
                if letter not in alphabet_list:
                    user_input = 'NONE'
                    print('Guess must be letters only')

        return user_input
    
    def get_right_letter_right_position(self):
        """
        Get information from user about which letters were correct.
        """
        user_input = 'NONE'
        while user_input == 'NONE':

            user_input = input('Letters in right position (enter \'h\' for help): ').upper()

            if user_input == 'H':
                print('Enter the letters that are in the right position guide')
                print('\tEnter positions that you have not solved for as a non letter character')
                print('\tIf you guessed \'CATER\', and E is in the right place')
                print('\tyou could enter ___E_, or 123e5 and so on.')
                user_input = 'NONE'

            elif len(user_input) != 5:
                user_input = 'NONE'
                print('Must be 5 characters long.')

            elif user_input in self.answer_list: # need to end stuff here
                print(f'It looks like we solved it! The answer was {user_input}')
                self.solved = True

        return user_input
            

    def get_right_letter_wrong_position(self):
        """
        Get information from user about which letters were just in the wrong position.
        """
        user_input = 'NONE'
        while user_input == 'NONE':

            user_input = input('Letters in wrong position (enter \'h\' for help): ').upper()

            if user_input == 'H':
                print('Enter the letters that are in the wrong position guide')
                print('\tEnter positions that you have not solved for as a non letter character')
                print('\tIf you guessed \'CATER\', and A is in the wrong place')
                print('\tyou could enter _A___, or 1a345 and so on.')
                user_input = 'NONE'

            elif len(user_input) != 5:
                user_input = 'NONE'
                print('Input must be 5 characters long.')

        return user_input

    def get_wrong_letter_wrong_position(self):
        """
        Get information from user about which letters are not in the word.
        """
        user_input = 'NONE'
        while user_input == 'NONE':

            user_input = input('Letters not in word (enter \'h\' for help): ').upper()

            if user_input == 'H':
                print('Enter the letters that are not in the word guide')
                print('\tEnter letters are in the word as a non letter character')
                print('\tIf you guessed \'CATER\', and R is not in the word')
                print('\tyou could enter ____R, or 1234r and so on.')
                user_input = 'NONE'

            elif len(user_input) != 5:
                user_input = 'NONE'
                print('Input must be 5 characters long.')

        return user_input

    def check_guess(self, guess, right_positions, right_letters, wrong_letters ):
        """
        Makes sure the information provided by the user is consistent.
        Parameters- 
            right_positions: letters in the right position.
            right_letters: letters whose position is not yet known.
            wrong_letters: letters not in the word.
        Returns-
            True if the information is consistent, False otherwise.
        """
        compiled_answer = ['*','*','*','*','*']

        for i in range(WORD_LENGTH):
            if right_positions[i] in alphabet_list:
                compiled_answer[i] = right_positions[i]

        for i in range(WORD_LENGTH):
            if right_letters[i] in alphabet_list:
                if compiled_answer[i] in alphabet_list:
                    print(f'conflicting status of correctness in {right_positions} and {right_letters}')
                else:
                    compiled_answer[i] = right_letters[i]

        for i in range(WORD_LENGTH):
            if wrong_letters[i] in alphabet_list:
                if compiled_answer[i] in alphabet_list:
                    print(f'Conflicting status of correctness in {wrong_letters} and ({right_positions} or {right_letters})')
                    return False
                else:
                    compiled_answer[i] = wrong_letters[i]
        final_compiled_answer = ''
        for letter in compiled_answer:
            final_compiled_answer += letter
        if final_compiled_answer == guess:
            return True
        else:
            return False

    def search_by_guess(self, right_pos_letters, right_letters, wrong_letters):
        """
        Search the lists based on input from the user.
        Parameters
            right_pos_letters: string. Alphabet characters in this indicate the position of letter in the word.
            right_letters: string. Alphabet characters indicate a letter that is in the wrong position.
            wrong_letters: string. Alphabet characters indicate a letter that is not in the word.
        """
        for i in range(WORD_LENGTH):
            if right_pos_letters[i] in alphabet_list:
                self.search_right_letter_right_position( right_pos_letters[i], i )
        for i in range(WORD_LENGTH):
            if right_letters[i] in alphabet_list:
                self.search_right_letter_wrong_position(right_letters[i], i)
        for i in range(WORD_LENGTH):
            if wrong_letters[i] in alphabet_list:
                self.search_wrong_letter_wrong_position(wrong_letters[i], i)

    def display_narrowed_answer_list_stats(self):
        """
        Display letter frequency stats for the narrowed answer list.
        """
        one_letter, two_letter, three_letter = self.letter_frequency()

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

    def letter_frequency(self):
        """
        Used to get the frequency of letters. 
        Parameters- none.
        Returns- 
            one_letter, two_letter, three_letter: lists that contain how often a letter appears
                once, twice, and thrice.
        """
        one_letter = [0 for i in range(26)]
        two_letter = [0 for i in range(26)]
        three_letter = [0 for i in range(26)]
        for letter in alphabet_list:
            for word in self.narrowed_answer_list:
                if word.count(letter) > 2:
                    three_letter[ alphabet_list.index(letter) ] += 1
                elif word.count(letter) > 1:
                    two_letter[ alphabet_list.index(letter) ] += 1
                elif word.count(letter) > 0:
                    one_letter[ alphabet_list.index(letter) ] += 1
        return one_letter, two_letter, three_letter

    def combined_frequency(self):
        """
        Returns the total number of words that contain each letter.
        """
        one_letter, two_letter, three_letter = self.letter_frequency()
        total_letters = [ one_letter[i] + two_letter[i] + three_letter[i] for i in range(26) ]
        return total_letters

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
    my_list.play_loop()