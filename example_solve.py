from wordle_solve import WORD_LENGTH, WordList
from wordle_solve import answers_list, guesses_list

def trial_1():
    # Using this to demonstrate solving for word "INERT"
    # Start our process by inputting the answers and guesses
    my_list = WordList( answers_list, guesses_list )
    # Need a second list to play with...
    second_list = WordList( my_list.answer_list, my_list.guess_list )
    # Get most common letters in second_list...
    print('Eliminating common letters')
    print(second_list.most_common_letters())
    # Search by 'E' in second_list, reprint
    second_list.search_letter('E')
    print(second_list.most_common_letters())
    # Repeat until we have 5 letters
    second_list.search_letter('R')
    print(second_list.most_common_letters())
    second_list.search_letter('A')
    print(second_list.most_common_letters())
    second_list.search_letter('T')
    print(second_list.most_common_letters())
    second_list.search_letter('C')
    print(second_list.most_common_letters())
    # Get potential guesses
    print('Good potential guesses: ')
    second_list.print_narrowed_answers()
    # Try "REACT"...
    # 'R', 'E' in wrong places, 'T' in right place, 'A', 'C' not in word.
    # Search our actual word list by it.
    my_list.search_right_letter_right_position('T',4)
    my_list.search_right_letter_wrong_position('R',0)
    my_list.search_right_letter_wrong_position('E',1)
    my_list.search_wrong_letter_wrong_position('A')
    my_list.search_wrong_letter_wrong_position('C')
    # Print out remainging answers just for kicks
    print('Possible words remaining: ')
    my_list.print_narrowed_answers()
    # Now we need a second guess informed by this one.
    # Start with getting most common remaining letters.
    print('Most common letters remaining: ')
    print( my_list.most_common_letters() )
    # Redo second list...
    second_list = WordList( my_list.narrowed_answer_list, my_list.narrowed_guess_list )
    second_list.search_letter('G')
    second_list.print_narrowed_answers()
    print( second_list.most_common_letters() )
    second_list.search_letter('E')
    print('More good guesses')
    second_list.print_narrowed_answers()
    # We can repeat all day, no need just pick one. Suppose we pick "EGRET"
    # One E in wrong place, G no in, R in wrong place, E 'not in', and T
    # Narrow by these...but not the second E we're not accounting for that yet... TODO: account for that
    my_list.search_right_letter_wrong_position('E',0)
    my_list.search_right_letter_wrong_position('E',3) # We can eliminate its wrong positions though
    my_list.search_right_letter_wrong_position('R',2)
    my_list.search_wrong_letter_wrong_position('G')
    # Print to see what's left.
    print('Remaining answers: ')
    my_list.print_narrowed_answers()
    # Observe that none of these are helpful...
    # But R has a most common position: position 3, which we aren't looking at yet.
    # TODO: account for most common positions.
    # At this point it's just a process of elimination, so I'd go 'OVERT', see that R is right and then try INERT
    # Now let's try looking at GUESSES and see if those are more helpful...
    print('Potential (but unhelpful in this case) guesses: ')
    my_list.print_narrowed_guesses()
    # They are not.
    # We need to look for words that have more of the most common letters besides ones
    #   we know are correct.

def trial_2():
    # TODO: implement this as a letter elimination guess optimizer.
    # Using this to demonstrate solving for word "INERT"
    # Start our process by inputting the answers and guesses
    my_list = WordList( answers_list, guesses_list )
    # Need a second list to play with...
    second_list = WordList( my_list.answer_list, my_list.guess_list )
    # Get most common letters in second_list...
    print('Eliminating common letters')
    print(second_list.most_common_letters())
    # Search by 'E' in second_list, reprint
    second_list.search_letter('E')
    print(second_list.most_common_letters())
    # Repeat until we have 5 letters
    second_list.search_letter('R')
    print(second_list.most_common_letters())
    second_list.search_letter('A')
    print(second_list.most_common_letters())
    second_list.search_letter('T')
    print(second_list.most_common_letters())
    second_list.search_letter('C')
    print(second_list.most_common_letters())
    # Get potential guesses
    print('Good potential guesses: ')
    second_list.print_narrowed_answers()
    # Try "REACT"...
    # 'R', 'E' in wrong places, 'T' in right place, 'A', 'C' not in word.
    # Search our actual word list by it.
    my_list.search_right_letter_right_position('T',4)
    my_list.search_right_letter_wrong_position('R',0)
    my_list.search_right_letter_wrong_position('E',1)
    my_list.search_wrong_letter_wrong_position('A')
    my_list.search_wrong_letter_wrong_position('C')
    # Print out remainging answers just for kicks
    print('Possible words remaining: ')
    my_list.print_narrowed_answers()
    # Now we need a second guess informed by this one.
    # Start with getting most common remaining letters.
    print('Most common letters remaining in my_list: ')
    print( my_list.most_common_letters() )
    # Redo second list...
    second_list.__reset__()
    # See if there are words without any of the letters
    for letter in my_list.found_letters:
        second_list.search_wrong_letter_wrong_position(letter)
    for letter in my_list.eliminated_letters:
        second_list.search_wrong_letter_wrong_position(letter)
    #print('These are good potential guesses from second_list, just need to be narrowed down')
    #second_list.print_narrowed_answers()
    print('Most common letters in second_list after narrowing: ')
    print( second_list.most_common_letters() )
    second_list.search_letter('Y')
    print( second_list.most_common_letters() )
    second_list.search_letter('L')
    print(second_list.most_common_letters())
    second_list.search_letter('O')
    print(second_list.most_common_letters())
    second_list.search_letter('D')
    print(second_list.most_common_letters())
    second_list.search_letter('G')
    print('More good guesses')
    second_list.print_narrowed_answers()
    # Now we're left with GODLY
    # All wrong
    my_list.search_wrong_letter_wrong_position('G')
    my_list.search_wrong_letter_wrong_position('O')
    my_list.search_wrong_letter_wrong_position('D')
    my_list.search_wrong_letter_wrong_position('L')
    my_list.search_wrong_letter_wrong_position('Y')
    # Print to see what's left.
    print('Remaining answers: ')
    my_list.print_narrowed_answers()
    # Now we need to account for multiple positions for sure.

def actual_2022_04_25():
    my_list = WordList(answers_list,guesses_list)
    second_list = WordList( my_list.narrowed_answer_list, my_list.narrowed_guess_list )
    print( second_list.most_common_letters() )
    letters = second_list.most_common_letters()
    for letter in letters:
        second_list.search_letter(letter)
    second_list.print_narrowed_answers()
    print('Used: REACT, EA are right, but wrong position.')
    my_list.search_right_letter_wrong_position('E',1)
    my_list.search_right_letter_wrong_position('A',2)
    my_list.search_wrong_letter_wrong_position('R')
    my_list.search_wrong_letter_wrong_position('C')
    my_list.search_wrong_letter_wrong_position('T')
    my_list.print_narrowed_answers()
    second_list = WordList(my_list.narrowed_answer_list,my_list.narrowed_answer_list)
    print(second_list.most_common_letters())
    second_list.search_letter('L')
    second_list.search_letter('G')
    second_list.search_letter('N')
    second_list.print_narrowed_answers()
    my_list.search_right_letter_right_position('A',0)
    my_list.search_right_letter_wrong_position('E',4)
    my_list.search_wrong_letter_wrong_position('N')
    my_list.search_wrong_letter_wrong_position('G')
    my_list.search_wrong_letter_wrong_position('L')
    my_list.print_narrowed_answers()
    second_list = my_list.copy()
    print( second_list.most_common_letters() )

def actual_2022_04_26():
    my_list = WordList(answers_list,guesses_list)
    second_list = WordList( my_list.narrowed_answer_list, my_list.narrowed_guess_list )
    print( second_list.most_common_letters() )
    letters = second_list.most_common_letters()
    for letter in letters:
        second_list.search_letter(letter)
    second_list.print_narrowed_answers()
    print('Used: REACT, E and T are right.')
    my_list.search_right_letter_right_position('E',1)
    my_list.search_right_letter_right_position('T',4)
    my_list.search_wrong_letter_wrong_position('R')
    my_list.search_wrong_letter_wrong_position('A')
    my_list.search_wrong_letter_wrong_position('C')
    my_list.print_narrowed_answers()
    print('Use DEBIT')
    print('I in wrong position')
    my_list.search_wrong_letter_wrong_position('D')
    my_list.search_wrong_letter_wrong_position('B')
    my_list.search_right_letter_wrong_position('I',3)
    second_list = my_list.copy()
    second_list.print_narrowed_answers()
    print('It is HEIST')

def test_get_guess():
    my_list = WordList(answers_list,guesses_list)
    print( my_list.get_best_guess() )

def actual_2022_04_27():
    my_list = WordList(answers_list,guesses_list)
    print(my_list.get_best_guess())
    my_list.search_wrong_letter_wrong_position('C')
    my_list.search_wrong_letter_wrong_position('A')
    my_list.search_wrong_letter_wrong_position('T')
    my_list.search_wrong_letter_wrong_position('E')
    my_list.search_wrong_letter_wrong_position('R')
    print(my_list.get_best_guess())
    my_list.search_wrong_letter_wrong_position('G')
    my_list.search_wrong_letter_wrong_position('D')
    my_list.search_wrong_letter_wrong_position('L')
    my_list.search_wrong_letter_wrong_position('Y')
    my_list.search_right_letter_wrong_position('O',1)
    print(my_list.get_best_guess())
    my_list.search_wrong_letter_wrong_position('P')
    my_list.search_right_letter_right_position('S',0)
    my_list.search_right_letter_right_position('O',2)
    my_list.search_right_letter_wrong_position('N',1)
    print(my_list.get_best_guess())
    print('And, SHOWN it is.')

if __name__ == '__main__':
    actual_2022_04_27()
    # TRIAL 1 is the winner, no more mass elimination of letters...for now.