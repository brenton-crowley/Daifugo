# coding=utf-8
"""*****************************************************************************

Project Three
Brenton Crowley 649683

Daifugo

*****************************************************************************"""

from itertools import cycle, product, groupby
from random import shuffle
from collections import defaultdict

SUITS = 'SHCD'
ORDERED_VALUES = '34567890JQKA2'

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
    pass


def generate_plays(hand):
    """Takes the single argument 'hand', which is a list of cards you currently
    hold, and returns a list of all possible (non-pass) plays (each of which is
    a list of cards).

    INPUTS:
        hand    - A list of cards you currently hold

    RETURNS
        list    - comprising of cards.
    """
    pass


def is_valid_play(play,rnd):
    """Should return a Boolean value, evaluating whether the given play is
    valid or not in the context of the current round. You may assume that play
    constitutes a legal combination of cards, including the possibility
    of a pass (play = None).

    INPUTS:
        play    - which is a play (i.e. a list of cards)
        rnd     - the round to date, in the form of a list of plays in
                  sequential order (each of which is, in turn, a list of cards)

    RETURNS
        bool    - evaluating whether the given play is valid or not in the
                  context of the current round
    """
    pass


def play(rnd, hand, discard, holding,
         generate=generate_plays, valid=is_valid_play):
    """This function is your game-playing agent, and returns your play in the
    form of a list of cards or None.

    'discard' represents the entire history of the game so far. It is a list,
    each element of which represents a round in order of play in the game.
    The first item is the first round, and the last item (discard[-1])
    represents the current round (and is identical to 'rnd').

    Your function should return a list of cards representing your next play.
    If you have no valid plays, or if you choose to pass, your function
    should return None.

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
    """Will return a tuple of lists whose length will be that
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

    print hands

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

    deck = product(ORDERED_VALUES, SUITS)
    deck = [''.join(card) for card in deck]

    if shouldShuffle:
        shuffle(deck)

    return deck


def sort_hand(hand):
    """Will mutate the `hand` by reordering according to the Diafugo rule of
    value ordering, which, in ascending order, is: 34567890JQKA2

    INPUTS:
        hand   - list of cards (e.g. "3D") to be sorted

    RETURNS
        None
    """

    groups = get_value_groups(hand)

    sorted_hand = []

    for key in ORDERED_VALUES:
        sorted_hand += groups[key]

    # reorders the supplied hand according to the sorted_hand
    for card in sorted_hand:
        index = sorted_hand.index(card)
        hand[index] = card

    return hand

def get_value_groups(hand):
    """
    Returns a dict containing the values in ORDERED_VALUES as keys. Each value
    in the dict will return a list of cards.

    e.g. {'J': ['JH, JS], '0': [0D] ...}

    INPUTS:
        hand    - list of cards (e.g. "3D")

    RETURNS:
        groups  - dict of lists
    """

    # create a dict to group values
    groups = defaultdict(list)

    # will get the key (first char of card) and append it to the containing list
    for rank, group in groupby(hand, lambda card: card[0]):
        groups[rank] += list(group)

    return groups
deal()