# coding=utf-8
"""*****************************************************************************

Project Three
Brenton Crowley 649683

Daifugo

*****************************************************************************"""

from itertools import cycle, product, groupby, combinations, chain, permutations
from random import shuffle
from collections import defaultdict


def swap_cards(hand, pid):
    """It returns a list of cards from hand to swap with an opposing player at
    the start of the game, based on the rules for card swapping.

    • Player 0 must give their two highest cards to Player 3
    • Player 1 must give their one highest card to Player 2
    • Player 2 must give one card of their choice to Player 1
    • Player 3 must give two cards of their choice to Player 0

    INPUTS:
        hand    - a list of cards (13 elements in total)
        pid     - an int between 0 and 3, inclusive, representing the player ID

    RETURNS
        list - comprising of cards.
    """

    sort_hand(hand)

    if pid == 0:
        return hand[-2:]
    elif pid == 1:
        return hand[-1:]
    elif pid == 2:
        # TODO will require more logic for strategy.
        # • You do not want to discard a card if it is part of a set,
        # or if it is part of n kind
        return hand[:1]
    elif pid == 3:
        # TODO will require more logic for strategy.
        # • You do not want to discard a card if it is part of a set,
        # or if it is part of n kind
        return hand[:2]
    else:
        return []


def generate_plays(hand):
    """Takes the single argument 'hand', which is a list of cards you currently
    hold, and returns a list of all possible (non-pass) plays (each of which is
    a list of cards).

    INPUTS:
        hand    - A list of cards you currently hold

    RETURNS
        list    - comprising of cards.
    """

    # add all the cards as single plays
    plays = [[card] for card in hand]

    # add all two,three and four-of-a-kind combinations
    plays += get_all_n_of_a_kind(hand)

    # add all the > 3 card straights
    plays += get_all_straights(hand)

    return plays


def get_last_live_play_from_rnd(rnd):
    """

    """
    decrementer = -1
    last_live_play = rnd[decrementer]

    while last_live_play is None:
        decrementer -= 1
        last_live_play = rnd[decrementer]

    return last_live_play


def is_valid_play(play, rnd):
    """
    Should return a Boolean value, evaluating whether the given play is
    valid or not in the context of the current round. Assume that play
    constitutes a legal combination of cards, including the possibility
    of a pass (play = None).

    If the comparison of the play and the last 'non-None-play) is valid then
    one can assume that the round is valid.

    INPUTS:
        play    - which is a play (i.e. a list of cards)
        rnd     - the round to date, in the form of a list of plays in
                  sequential order (each of which is, in turn, a list of cards)

    RETURNS
        bool    - evaluating whether the given play is valid or not in the
                  context of the current round
    """

    # Lead case: invalid if no plays in round and play is None
    if play is None and len(rnd) == 0:
        return False
    elif play is not None and len(rnd) == 0:
        return True

    # Assume at least one play has been made, and last_live_play
    # is the last non-pass play
    decrementer = -1
    last_live_play = get_last_live_play_from_rnd(rnd)

    # n-of-a-kind case
    if get_play_n_of_a_kind(play) > 1:
        if get_play_n_of_a_kind(play) == get_play_n_of_a_kind(last_live_play):

            played_rank = get_rank_dict(play).keys()[0]
            last_live_rank = get_rank_dict(last_live_play).keys()[0]

            if ORDERED_RANKS.index(played_rank) > \
                    ORDERED_RANKS.index(last_live_rank):
                return True

    # assume no n-of-a-kind. Now either a straight or single card
    if is_play_straight(play) and is_play_straight(last_live_play):

        highest_played_card = play[-1]
        highest_last_live_card = last_live_play[-1]

        played_rank = highest_played_card[0]
        last_live_rank = highest_last_live_card[0]

        if ORDERED_RANKS.index(played_rank) > \
                ORDERED_RANKS.index(last_live_rank):

            if is_round_on_suit(rnd):

                played_suit = highest_played_card[1]
                last_live_suit = highest_last_live_card[1]

                if played_suit != last_live_suit:
                    return False

            return True


    else:
        pass


    return False

# TODO perhaps find a cleaner solution
def is_round_on_suit(rnd):
    """
    Returns a boolean indicating whether or not the round is on suit.
    If the second play of the round follows the same suit as the first
    play then the round is deemed to be 'on suit'

    INPUTS:
        rnd     - the round to date, in the form of a list of plays in
              sequential order (each of which is, in turn, a list of cards)

    RETURNS:
        bool    - True if round is 'on_suit' otherwise False
    """

    if rnd is None:
        return False

    # if the rnd has fewer than two plays then it cannot be 'on suit'
    if len(rnd) < 2:
        return False

    opening_play = rnd[0]
    next_play = None

    for i in range(1, len(rnd)):

        play = rnd[i]

        if play is not None:
            next_play = play
            break

    if next_play is None:
        return False

    if opening_play[0][1] != next_play[0][1]:
        return False

    return True


def is_play_n_of_a_kind(play, n):
    """
    Returns a boolean indicating whether or not the play is `n`-of-a-kind.

    INPUTS:
        play    - the play to validate.
        n       - the delimiter

    RETURNS:
        bool    - True if play is n-of-a-kind otherwise False
    """

    # if the rnd has fewer than two plays then it cannot be 'on suit'
    if play is None:
        return False

    if get_play_n_of_a_kind(play) != n:
        return False

    return True


def is_play_straight(play):
    """
    Returns a boolean indicating whether or not the play is a straight

    INPUTS:
        play    - the play to validate.

    RETURNS:
        bool    - True if play is a straight otherwise False
    """

    if play is None:
        return False

    suit_dict = get_suit_dict(play)

    # must be a flush i.e. all one suit
    if len(suit_dict.keys()) != 1:
        return False

    ranks = suit_dict.values()[0]

    # straight must have a minimum of 3 cards
    if len(ranks) < 3:
        return False

    ranks.sort(key=SORT_FIRST_ELEMENT_BY_RANK)
    straight = "".join(ranks)

    return straight in ORDERED_RANKS


def get_play_n_of_a_kind(play):
    """
    Returns an int that corresponds to the `n` repeats of a rank in a play.

    If the play is a None oro invalid then 0.
    If the play is a single card then 1.
    If the play is a two-of-a-kind then 2 is returned.
    If the play is a three-of-a-kind then 3 is returned.
    If the play is a four-of-a-kind then 4 is returned.

    INPUTS:
        play    - the play to validate. ['5H']

    RETURNS:
        int     - int that corresponds to the n-of-a-kind (0-4)
    """

    # if the rnd has fewer than two plays then it cannot be 'on suit'
    if play is None:
        return 0

    rank_dict = get_rank_dict(play)

    # must have only rank to be n-of-a-kind
    if not 0 < len(rank_dict.keys()) < 2:
        return 0

    return len(rank_dict.values()[0])


def play(rnd, hand, discard, holding,
         generate=generate_plays, valid=is_valid_play):
    """This function is the game-playing agent, and returns the play in the
    form of a list of cards or None.

    'discard' represents the entire history of the game so far. It is a list,
    each element of which represents a round in order of play in the game.
    The first item is the first round, and the last item (discard[-1])
    represents the current round (and is identical to 'rnd').

    The function should return a list of cards representing the next play.
    If there are no valid plays, or if a pass is chosen, the function
    will return None.

    INPUTS:
        rnd     - a list of plays from the round to date
        hand    - a list of the current cards held by your player
        discard - a list of the history of the game so far
        holding - a 4-tuple made up of int values representing how many cards
                  each of the players is holding, indexed by the player ID
        generate- which defaults to generate_plays function
        valid   - which defaults to is_valid_play function

    RETURNS
        list    - list of cards representing the next play.
    """
    pass


def deal(players=4):
    """
    Will return a tuple of lists whose length will be that
    of the `players` input, which defaults to 4. Each nested list will comprise
    cards whose length is determined by the quotient of the number of players
    over the deck length (52).

    INPUTS:
        players - the number of players to deal to

    RETURNS:
        list    - a tuple of lists.
    """
    deck = get_deck(True)
    hands = list(list() for i in xrange(players))
    players = cycle(hands)

    for card in deck:
        player = players.next()
        player.append(card)

    for hand in hands:
        sort_hand(hand)
        generate_plays(hand)

    return hands


def get_deck(shouldShuffle=False):
    """Will return a list of strings in the form of '"value" + "suit"' e.g. "3D"
    which signifies 3 of diamonds. The value 0 is equivalent to 10.

    INPUTS:
        shouldShuffle   - boolean that determines whether or not the deck order
                          is randomised.

    RETURNS
        list            - list of strings exactly 52 in length.
    """

    deck = product(ORDERED_RANKS, SUITS)
    deck = [''.join(card) for card in deck]

    if shouldShuffle:
        shuffle(deck)

    return deck


def sort_hand(hand):
    """Will mutate the `hand` according to the Diafugo rule of
    value ordering, which, in ascending order, is: 34567890JQKA2

    It uses `SORT_FIRST_ELEMENT_BY_RANK` constant function as its sort key,
    which looks up the index of the rank in ORDERED_RANKS.

    It is wrapped in a function since it is used more than once, so it is
    easier to modify this function if a change is required.

    INPUTS:
        hand   - list of cards (e.g. ['3D', 'JH]', '2C') to be sorted

    RETURNS
        None
    """

    hand.sort(key=SORT_FIRST_ELEMENT_BY_RANK)


def get_rank_dict(hand):
    """
    Returns a dict containing the ranks in ORDERED_RANKS as keys. Each value
    in the dict will return a list of cards.

    e.g. {'J': ['H', 'S'], '0': ['D'] ...}

    INPUTS:
        hand    - list of cards (e.g. ['3D'])

    RETURNS:
        groups  - dict of lists
    """

    if len(hand) == 1 and hand[0] is None:
        return {}

    # create a dict to group values
    rank_dict = defaultdict(list)

    # will get the key (first char of card) and append it to the containing list
    for rank, group in groupby(hand, lambda card: card[0]):
        rank_dict[rank] += [card[1] for card in group]
        # print (rank, group)

    return rank_dict


def get_suit_dict(hand):
    """
    Returns a dict containing the values in SUITS as keys. Each value
    in the dict will return a list of cards.

    e.g. {'H': ['3', '4'], '0': ['D'] ...}

    INPUTS:
        hand    - list of cards (e.g. ['3D'])

    RETURNS:
        groups  - dict of str lists
    """

    if len(hand) == 1 and hand[0] is None:
        return {}

    # create a dict to group values
    suit_dict = defaultdict(list)

    # will get the suit (second char of card) and append it to the
    # containing list
    for suit, cards in groupby(hand, lambda card: card[1]):
        suit_dict[suit] += [card[0] for card in cards]

    return suit_dict


def get_all_n_of_a_kind(hand):
    """
    Returns a list containing the all the possible combinations of n-of-a-kind.
    Two-of-a-kind: ['3H', '3D']
    Three-of-a-kind: ['5D', '5H', '5S']
    Four-of-a-kind: ['JD', 'JH', 'JS', 'JC']

    INPUTS:
        hand    - list of cards (e.g. ['3D'])

    RETURNS:
        groups  - list of lists
    """
    rank_dict = get_rank_dict(hand)

    all_combinations = []

    for rank in rank_dict.keys():

        # need to combine the ranks and suits
        cards = [rank + suit for suit in rank_dict[rank]]

        if len(cards) >= 2:  # two or more get all 2-of-a-kind
            all_combinations += combinations(cards, 2)

        if len(cards) >= 3:  # three or more get all 3-of-a-kind
            all_combinations += combinations(cards, 3)

        if len(cards) == 4:  # 4-of-a-kind
            all_combinations += [cards]

    return all_combinations


def get_all_straights(hand):
    """
    Returns a list containing the all the possible straight combinations
    of which straight length is greater than 2

    e.g. [['3D', '4D', '5D'], ['7C', '8C', '9C', '0C']]

    INPUTS:
        hand    - list of cards (e.g. ['3D', '5S', '7C'])

    RETURNS:
        groups  - list of lists
    """

    def get_straight_possibilities(ranks):
        """
        Returns the potential straight powerset combinations in lists where
        the minimum length of a straight must be 3.

        Combinations is used over Permutations to reduce the overhead of
        possible_straights. To overcome the possibility that a combination
        may not be ordered, the resulting straight combination is sorted in the
        body of `find_all_straights`

        INPUTS:

            ranks      - list of ranks e.g. ['3', '4', '5', 'J', 'Q', 'K']

        RETURNS:
            iterator   - iterator of all valid and invalid straight combinations

        """
        straight_range = range(3, len(ranks) + 1)

        return chain.from_iterable(
            combinations(
                ranks, straight_length) for straight_length in straight_range)

    all_straights = []

    # no possibility of a straight if there are less than 3 cards.
    if len(hand) < 3:
        return all_straights

    suit_dict = get_suit_dict(hand)  # suit as key, rank as value e.g. {'H':[0]}

    for suit in suit_dict:

        ranks = suit_dict[suit]

        if len(ranks) < 3:
            continue

        # `s` is a straight_possibility
        # i.e. a tuple of ranks in the straight powerset
        for s in get_straight_possibilities(ranks):

            # sort the sequence as it could be jumbled
            s = list(s)
            s.sort(key=SORT_FIRST_ELEMENT_BY_RANK)

            straight = "".join(s)

            if straight in ORDERED_RANKS:
                all_straights.append(
                    ["".join(card) for card in product(straight, suit)])

    return all_straights


# CONSTANTS

SUITS = 'SHCD'
ORDERED_RANKS = '34567890JQKA2'
SORT_FIRST_ELEMENT_BY_RANK = \
    lambda string: ORDERED_RANKS.index(string[0])  # e.g. ['2H']

deal()

# print get_all_straights(['3H', '4H', '5H', 'JH', 'QH', 'KH'])
# print get_all_straights(["2H", "AH", "KH", "QH", "JH", "0H", "9H"])

# print is_play_n_of_a_kind(["5S"], 2)
# print is_play_n_of_a_kind(["5S", "5C"], 2)
# print is_play_n_of_a_kind(["5S", "5C", "5H"], 2)
# print is_play_n_of_a_kind(["5S", "5C", "5H", "5C"], 2)
# print is_play_n_of_a_kind(["5S"], 2)
# print is_play_n_of_a_kind(None, 2)
#
# print is_play_n_of_a_kind(["5S"], 3)
# print is_play_n_of_a_kind(["5S", "5C"], 3)
# print is_play_n_of_a_kind(["5S", "5C", "5H"], 3)
# print is_play_n_of_a_kind(["5S", "6S", "7S"], 3)
# print is_play_n_of_a_kind(["5S", "5C", "5H", "5C"], 3)
# print is_play_n_of_a_kind(["5S"], 3)
# print is_play_n_of_a_kind(None, 3)
#
# print is_play_n_of_a_kind(["5S"], 4)
# print is_play_n_of_a_kind(["5S", "5C"], 4)
# print is_play_n_of_a_kind(["5S", "5C", "5H"], 4)
# print is_play_n_of_a_kind(["5S", "5C", "5H", "5C"], 4)
# print is_play_n_of_a_kind(["5S"], 4)
# print is_play_n_of_a_kind(None, 4)

# print is_play_straight(['3H', '4H', '5H', 'JH', 'QH', 'KH'])  # False
# print is_play_straight(["2H", "AH", "KH", "QH", "JH", "9H", "0H"])  # True

# print is_round_on_suit([["5S", "5C", "5H"]])  # False only one play
# print is_round_on_suit([["5S", "5C", "5H"], ["6S", "6C", "6H"]])  # False
# print is_round_on_suit([["5S"], ["6S"]])  # True
# print is_round_on_suit([["5S", "6S", "7S"], ["8S", "9S", "0S"]])  # True
# print is_round_on_suit([["5S", "6S", "7S"], [None]])  # False

# print get_play_n_of_a_kind(["3S"])  # return 1
# print get_play_n_of_a_kind(["3S", "3H"])  # return 2
# print get_play_n_of_a_kind(["3S", "3H", "3D"])  # return 3
# print get_play_n_of_a_kind(["3S", "3H", "3D", "3C"])  # return 4
# print get_play_n_of_a_kind(["5S", "6S", "7S"])  # return 0
# print get_play_n_of_a_kind([None])  # return 0

print is_valid_play(["7H", "7C"],[["5S", "5C"],["6H", "6C"], None])  # True
print is_valid_play(["2H", "2C"],[["5S", "5C"],["JH", "JC"], None])  # True
print is_valid_play(["JD", "JS"],[["JH", "JC"], None])  # False

print is_valid_play(["4D", "5D", "6D", "7D", "8D"],
                    [["5H", "6H", "7H"], None])  # True

print is_valid_play(["QC", "KC", "AC"],
                    [["5H", "6H", "7H"], None, ["9H", "0H", "JH"]])  # False
