"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

from Card import *

class PokerHand(Hand):
    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.

        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1

    def rank_hist(self):
        """Builds a histogram of the ranks that appear in the hand.

        Stores the result in attribute ranks.
        """
        self.ranks = {}
        for card in self.cards:
            self.ranks[card.rank] = self.ranks.get(card.rank, 0) + 1

    def rank_given_suit_hist(self, suit):
        """Builds a histogram of the ranks of a given suit that appear in the hand.

        Stores the result in attribute ranks_given_suit under the suit as key.
        """
        result = {}
        for card in self.cards:
            if card.suit == suit:
               result[card.rank] = result.get(card.rank, 0) + 1
        try:
            self.ranks_given_suit[suit] = result
        except:
            self.ranks_given_suit = {}
            self.ranks_given_suit[suit] = result

    def has_nothing(self):
        return True

    def has_pair(self):
        self.rank_hist()
        pairs = [i for i in self.ranks.values() if i >= 2]
        return len(pairs) >= 1

    def has_two_pair(self):
        self.rank_hist()
        pairs = [i for i in self.ranks.values() if i >= 2]
        return len(pairs) >= 2

    def has_three_of_a_kind(self):
        self.rank_hist()
        triples = [i for i in self.ranks.values() if i >= 3]
        return len(triples) >= 1

    def has_straight(self, suit=None):
        if suit == None:
            self.rank_hist()
            cardlist = self.ranks
        else:
            self.rank_given_suit_hist(suit)
            cardlist = self.ranks_given_suit[suit]

        indices = range(1,14)+[1]
        for i in xrange(len(indices)-4):
            mylist = [cardlist.get(indices[i+j], None) for j in xrange(5)]
            if None in mylist:
                continue
            return True
        return False

    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False

    def has_full_house(self):
        self.rank_hist()
        pairs = [i for i in self.ranks.values() if i >= 2]
        triples = [i for i in self.ranks.values() if i >= 3]
        # Note that a triple will appear as a pair, we need 
        # to make sure we don't double count
        return len(pairs) >= 2 and len(triples) >= 1

    def has_four_of_a_kind(self):
        self.rank_hist()
        quadruples = [i for i in self.ranks.values() if i >= 4]
        return len(quadruples) >= 1

    def has_straight_flush(self):
        for suit in xrange(len(Card.suit_names)):
            self.rank_given_suit_hist(suit)
            result = self.has_straight(suit)
            if result:
                return True
        return False

    handChecks = (has_straight_flush,
                  has_four_of_a_kind, 
                  has_full_house, 
                  has_flush, 
                  has_straight, 
                  has_three_of_a_kind, 
                  has_two_pair,
                  has_pair,
                  has_nothing)

    handLabels = ("straight flush", 
                  "four of a kind", 
                  "full house", 
                  "flush", 
                  "straight", 
                  "three of a kind", 
                  "two pair", 
                  "pair",
                  "nothing")

    def classify(self):
        for func, name in zip(self.handChecks, self.handLabels):
            if func(self):
                self.label = name
                return

def estimateProbabilities(cardsPerHand=5, runs=1000, seed=42):
    random.seed(seed)
    print "Poker hand estimation"
    print "Parameters:\n   cardsPerHand: %d\n   runs: %d\n   seed: %d\n" %(cardsPerHand, runs, seed)

    # Prep a result dict
    result = {}
    for label in PokerHand.handLabels:
        result[label] = 0

    for _ in xrange(runs):
        deck = Deck()
        deck.shuffle()       
        for i in range(52/cardsPerHand):
            hand = PokerHand()
            deck.move_cards(hand, cardsPerHand)
            hand.classify()
            result[hand.label] += 1
    # Compute percentages
    for key,value in result.items():
        result[key] = value/(runs*(10.0))*100
    return result

def nicePrint(result):
    print "%-18s %-8s\n%-18s %-8s" % ("Label", "Percent", "-"*18, "-"*8)
    for label in PokerHand.handLabels:
        print "%-18s %0.4f%%" % (label, result[label])

if __name__ == '__main__':
    runs = 10000
    nicePrint(estimateProbabilities(runs=runs))