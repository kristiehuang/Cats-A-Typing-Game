"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    if len(paragraphs) < k + 1:
        return ''
    n = -1
    for parag in paragraphs:
        if select(parag):
            n += 1
        if n == k:
            return parag
    return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def check_contains(string):
        for word in topic:
            for word2 in split(remove_punctuation(string)):
                if lower(word) == lower(word2):
                    return True
        return False
    return check_contains
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    i = 0
    correct = 0
    if len(typed_words) == 0:
        return 0.0
    while i < min(len(reference_words), len(typed_words)):
        if typed_words[i] == reference_words[i]:
            correct += 1
        i +=1
    return correct*100 / len(typed_words)
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    if typed == '':
        return 0.0
    return len(typed) * (60/elapsed) / 5
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    lowest_diff, lowest_word = len(user_word), user_word
    for word in valid_words:
        if user_word == word:
            return word
        diff = diff_function(user_word, word, limit)
        if diff < lowest_diff:
            lowest_diff = diff
            lowest_word = word
    if lowest_diff > limit:
        return user_word
    else:
        return lowest_word
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    #assert False, 'Remove this line'
    def swap_helper(index, letters_left):
        if index < len(start) and index < len(goal) and letters_left >= 0: #index in bounds
            if start[index] != goal[index]:
                return 1 + swap_helper(index+1, letters_left-1)
            else:
                return swap_helper(index+1, letters_left)
        else: #IF NEXT INDEX WILL BE OUT OF BOUNDS
            return abs(len(start) - len(goal))

    return swap_helper(0, limit)
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    #assert False, 'Remove this line'

    if start == goal:
        return 0
    elif limit < 0:
        return 0
    elif len(start) == 0 or len(goal) == 0: #to add digits or subtract digits
        return abs(len(goal) - len(start))
    elif start[0] == goal[0]:
        return edit_diff(start[1:], goal[1:], limit)
    else:
        add_diff = 1 + edit_diff(goal[0] + start, goal, limit-1)
        remove_diff = 1 + edit_diff(start[1:], goal, limit-1)
        substitute_diff = 1 + edit_diff(goal[0] + start[1:], goal, limit-1)
        return min(add_diff, remove_diff, substitute_diff)

    # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    i, count = 0, 0
    for n in typed:
        if n == prompt[i]:
            count += 1
        else:
            send({'id': id, 'progress': count / len(prompt)})
            return count / len(prompt)
        i += 1

    send({'id': id, 'progress': count / len(prompt)})
    return count / len(prompt)
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    def time_spent_typing_word(i, player):
        return elapsed_time(word_times[player][i]) - elapsed_time(word_times[player][i-1])
    def fastest_time_for_word(i):
        time_arr = [time_spent_typing_word(i, player) for player in range(n_players)]
        return min(time_arr)
    def is_fastest(i, player):
        return abs(time_spent_typing_word(i, player) - fastest_time_for_word(i)) <= margin

    words = [word(i) for i in word_times[0]]
    return [[words[i] for i in range(1, n_words+1) if is_fastest(i, p)] for p in range(n_players)]
    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
