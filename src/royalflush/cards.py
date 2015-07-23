##encoding=utf-8

from __future__ import print_function
from royalflush.glossary import glossary
from royalflush.bitmath import create_bitmap
import itertools
import random
import hashlib


class InvalidCardError(Exception):
	pass

class InvalidHandError(Exception):
	pass

class EmptyDeckError(Exception):
	pass

class InvalidPokerHandError(Exception):
	pass

class Card():
	def __init__(self, suit, rank):
		# check input
		if not (isinstance(suit, int) and isinstance(rank, int)):
			raise InvalidCardError("suit and rank has to be integer.")
		if rank == 1:
			rank += 13
		if not (1 <= suit <= 4):
			raise InvalidCardError(
				"suit=%s, rank=%s is not a valid card." % (suit, rank))
		if not (2 <= rank <= 14):
			raise InvalidCardError(
				"suit=%s, rank=%s is not a valid card." % (suit, rank))

		self._suit = suit
		self._rank = rank
	
	@property
	def suit(self):
		return self._suit
	
	@property
	def rank(self):
		return self._rank
		
	def __str__(self):		
		return "%s of %s" % (glossary.card_rank_alias[self._rank],
							 glossary.card_suit_alias[self._suit],)
	
	def icon(self):
		return "%s %s" % (glossary.card_suit_icon_alias[self._suit],
						  glossary.card_rank_icon_alias[self._rank],)
	
	def __repr__(self):
		return "Card(suit=%s, rank=%s)" % (self._suit, self._rank)

	@staticmethod
	def random():
		"""generate a random card
		"""
		return Card(suit=random.randint(1, 4), rank=random.randint(1, 13))
	
	def __hash__(self):
		"""hash method, set operation support
		"""
		return self._rank * 4 + self._suit
	
	def __eq__(self, other):
		try:
			return hash(self) == hash(other)
		except:
			raise Exception("Cannot compare %s with %s." % (repr(self), repr(other)))
	
	def __lt__(self, other):
		return hash(self) < hash(other)

	def __le__(self, other):
		return hash(self) <= hash(other)
	
	def __gt__(self, other):
		return hash(self) > hash(other)
	
	def __ge__(self, other):
		return hash(self) >= hash(other)

_CARD_CODES = dict()
for rank in range(2, 14+1):
	for suit in range(1, 4+1):
		c = Card(suit=suit, rank=rank)
		_CARD_CODES[hash(c)] = c

class Hands(object):
	_max_cards = 52
	def __init__(self, cards=list()):
		# check input
		if not isinstance(cards, list):
			raise InvalidHandError("You cannot initiate a Hands with a non-Card-List")
		
		if len(cards) > self._max_cards:
			raise InvalidHandError("A hands cannot have more than %s cards." % self._max_cards)
		
		for item in cards:
			if not isinstance(item, Card):
				raise InvalidHandError("You cannot initiate a Hands with list of "
									   "object other than Card.")
		
		self.cards = list()
		for card in cards:
			self.cards.append(card)
		
	def __str__(self):
		lines = list()
		for i, card in enumerate(self.cards):
			lines.append("%s. %s" % (i+1, card))
		return "\n".join(lines)
	
	def __repr__(self):
		return "Hands(cards=%s)" % repr(self.cards)
	
	def icon(self):
		return "".join(["[%s]" % card.icon() for card in self.cards])
	
	@staticmethod
	def random(n=5, non_repeat=True):
		if n > Hands._max_cards:
			raise InvalidHandError("A hands cannot have more than %s cards." % Hands._max_cards)
		
		if non_repeat:
			cards = set()
			while 1:
				cards.add(Card.random())
				if len(cards) == n:
					break
			return Hands(list(cards))
		else:
			cards = [Card.random() for _ in range(n)]
			return Hands(cards)
	
	def __len__(self):
		return len(self.cards)
	
	def __iter__(self):
		for card in self.cards:
			yield card
	
	def __getitem__(self, key):
		return self.cards[key]
	
	def shuffle(self):
		random.shuffle(self.cards)
	
	def sort(self):
		self.cards.sort()
	
	def add_card(self, card):
		"""add one card
		"""
		if not isinstance(card, Card):
			raise Exception("You can only add a Card or Hands object to a Hands object.")
		
		if len(self.cards) == 52:
			raise InvalidHandError("A hands cannot have more than %s cards." % self._max_cards)
		
		self.cards.append(card)
		
	def add_hands(self, hands):
		"""add hand of cards, i.e. multiple cards
		"""
		if not isinstance(hands, Hands):
			raise Exception("You can only add a Card or Hands object to a Hands object.")
		
		for card in hands:
			self.add_card(card)
	
	def pick_best_pokerhand(self):
		"""
		"""
		cards_in_hand = set(self.cards)
		if len(cards_in_hand) < 5:
			raise Exception("For picking a poker hands, you have to have at least 5 "
							"different cards.")
		
		if len(cards_in_hand) > 26:
			print("Warning, picking the best pokerhand from more than 26 cards is slow.")
		
		pokerhand = None
		for cards in itertools.combinations(cards_in_hand, 5):
			p = PokerHand(Hands(list(cards)))
			try:
				if pokerhand <= p:
					pokerhand = p
			except:
				pokerhand = p
		return pokerhand
	
	def __hash__(self):
		return hash("-".join([str(hash(card)) for card in self.cards]) )
	
	def sign(self):
		return "-".join([str(hash(card)) for card in self.cards])
	
	def hash(self):
		return hash("-".join([str(hash(card)) for card in self.cards]) )
	
	def md5(self):
		m = hashlib.md5()
		for card in self.cards:
			m.update(bytes(hash(card)))
		return m.hexdigest()
	
	def bitmap(self):
		value = 0
		for card in self.cards:
			value += 1 << (hash(card) - 1)
		return value

class Deck(Hands):
	_max_cards = 1 << 10
	def __init__(self, n=1, shuffle=True):
		"""initiate a deck of cards. you can name how many deck you want to use
		"""
		cards = list()
		for _ in range(n):
			for suit in range(1, 4+1):
				for rank in range(1, 13+1):
					cards.append(Card(suit=suit, rank=rank))
		self.cards = cards[::-1]
		if shuffle:
			self.shuffle()

	def deal_card(self):
		try:
			return self.cards.pop()
		except:
			raise EmptyDeckError("Cannot deal card from an empty deck.")
		
	def deal_hands(self, n):
		if len(self.cards) < n:
			raise EmptyDeckError("Not enough cards for dealing %s cards" % n)
		
		cards = list()
		for _ in range(n):
			cards.append(self.deal_card())
		return Hands(cards=cards)
	

class PokerHand():
	_weight1 = 14 ** 5 # a poker hand has 10 possible patterns, which gives highest weight
	_weight2 = 14 ** 4 # there are 5 cards at most in calculating the score
	_weight3 = 14 ** 3
	_weight4 = 14 ** 2
	_weight5 = 14 ** 1
	_weight6 = 14 ** 0
	
	def __init__(self, hands):
		"""initiate a poker hand. a valid poker hand meets:
			1. 5 different cards.
			2. no Joker
		"""
		if not isinstance(hands, Hands):
			raise InvalidPokerHandError("You can only initiate a PockerHand "
										 "with hands of 5 cards.")
		if len(set(hands.cards)) != 5:
			raise InvalidPokerHandError("A PokerHand cannot have repeat cards.")
			
		self.cards = list(hands.cards)
		self.detect()
		self.pattern = glossary.pokerhand_alias[self.strength]
		
	def __str__(self):
		h = Hands(self.cards)
		return "%s, type = '%s', score = %s" % (
					h.icon(), glossary.pokerhand_alias[self.strength], self.score)
	
	def icon(self):
		"""print utf-8 icon of a poker hand
		"""
		return "".join(["[%s]" % card.icon() for card in self.cards])
	

	def hist(self, array):
		"""frequency analysis function
		"""
		d = dict()
		for i in array:
			try:
				d[i] += 1
			except:
				d[i] = 1
		return d
	
	def detect(self):
		"""detect the pattern of the poker hand, and also calculate the score.
		large score beat small score
		"""
		# 1. 先取得牌型分
		# 2. 再算牌型中三张的那张牌的分
		# 3. 再按照从大到小的顺序计算剩下次要的牌的分
		
		self.strength = 0
		self.score = 0
		
		suit_histgram = self.hist([card.suit for card in self.cards])
		histgram = self.hist([card.rank for card in self.cards])
		
		##############################################################
		# Try to detect flush, straight, straight flush, royal flush #
		##############################################################
		if len(suit_histgram) == 1: # FLUSH or bigger
			if len(histgram) == 5: # possibly straight flush
				rank_list = list(histgram.keys())
				if 14 in rank_list: # if Ace in it, it can be 1 also
					rank_list.append(1)
				rank_list.sort()
				
				chain = [-999]
				
				for rank in rank_list:
					if (rank - chain[-1]) == 1:
						chain.append(rank)
						if len(chain) == 5:
							break
					else:
						chain.clear()
						chain.append(rank)
						
				if len(chain) == 5: # there's a straight
					if chain[0] == 10: # <ROYAL FLUSH> DETECTED!
						self.strength = 10
						self.score += self.strength * self._weight1
						return
					else: # <STRAIGHT FLUSH> DETECTED!
						self.strength = 9
						self.score += self.strength * self._weight1
						self.score += chain[0] * self._weight2
						return
				else: # <FLUSH> DETECTED!
					self.strength = 6
					self.score += self.strength * self._weight1
					
					minion = list(histgram.keys())
					minion.sort(reverse=True)
					
					self.score += minion[0] * self._weight2
					self.score += minion[1] * self._weight3
					self.score += minion[2] * self._weight4
					self.score += minion[3] * self._weight5
					self.score += minion[4] * self._weight6
					return
				
			else: # <FLUSH> DETECTED!
				self.strength = 6
				self.score += self.strength * self._weight1
				
				minion = list(histgram.keys())
				minion.sort(reverse=True)
				
				self.score += minion[0] * self._weight2
				self.score += minion[1] * self._weight3
				self.score += minion[2] * self._weight4
				self.score += minion[3] * self._weight5
				self.score += minion[4] * self._weight6
				return
			
		else: # try to detect Straight
			rank_list = list(histgram.keys())
			if 14 in rank_list: # if Ace in it, it can be 1 also
				rank_list.append(1)
			rank_list.sort()
			
			chain = [-999]
			
			for rank in rank_list:
				if (rank - chain[-1]) == 1:
					chain.append(rank)
					if len(chain) == 5:
						break
				else:
					chain.clear()
					chain.append(rank)
					
			if len(chain) == 5: # <STRAIGHT> DETECTED!
				self.strength = 5
				self.score += self.strength * self._weight1
				self.score += chain[0] * self._weight2
				return
		
		
		###############################
		# Try to detect other pattern #
		###############################
		values = set(histgram.values())

		if len(histgram) == 2: # 4 of a Kind or Full House
			values = set(histgram.values())
			
			if values == {1, 4}: # <4 OF A KIND> DETECTED!
				self.strength = 8
				self.score += self.strength * self._weight1
				
				for rank, repeat in histgram.items():
					if repeat == 4:
						self.score += rank * self._weight2
					else: # repeat = 1
						self.score += rank * self._weight3
				return
			
			elif values == {2, 3}: # <FULL HOUSE> DETECTED!
				self.strength = 7
				self.score += self.strength * self._weight1
				
				for rank, repeat in histgram.items():
					if repeat == 3:
						self.score += rank * self._weight2
					else: # repeat = 2
						self.score += rank * self._weight3
				
			else:
				raise Exception("god")
				
		elif len(histgram) == 3: # 3 of a Kind or 2 pair
			values = set(histgram.values())
			
			if values == {1, 3}: # <3 OF A KIND> DETECTED!
				self.strength = 4
				self.score += self.strength * self._weight1
				
				minion = list()
				for rank, repeat in histgram.items():
					if repeat == 3:
						self.score += rank * self._weight2
					else:
						minion.append(rank)
				minion.sort(reverse=True)
				
				self.score += minion[0] * self._weight3
				self.score += minion[1] * self._weight4
				
			elif values == {1, 2}: # <2 PAIR> DETECTED!
				self.strength = 3
				self.score += self.strength * self._weight1
				
				minion = list()
				for rank, repeat in histgram.items():
					if repeat == 1:
						self.score += rank * self._weight4
					else:
						minion.append(rank)
				minion.sort(reverse=True)

				self.score += minion[0] * self._weight2
				self.score += minion[1] * self._weight3
			else:
				raise Exception("god")
			
		elif len(histgram) == 4: # <1 PAIR> DETECTED!
			self.strength = 2
			self.score += self.strength * self._weight1
			
			values = set(histgram.values())
			minion = list()
			for rank, repeat in histgram.items():
				if repeat == 2:
					self.score += rank * self._weight2
				else:
					minion.append(rank)
			minion.sort(reverse=True)

			self.score += minion[0] * self._weight3
			self.score += minion[1] * self._weight4
			self.score += minion[2] * self._weight5
			
		elif len(histgram) == 5: # <HIGH CARD> DETECTED!
			self.strength = 1
			self.score += self.strength * self._weight1
			
			minion = list(histgram.keys())
			minion.sort(reverse=True)
			
			self.score += minion[0] * self._weight2
			self.score += minion[1] * self._weight3
			self.score += minion[2] * self._weight4
			self.score += minion[3] * self._weight5
			self.score += minion[4] * self._weight6
	
	def __eq__(self, other):
		return self.score == other.score

	def __lt__(self, other):
		return self.score < other.score
	
	def __le__(self, other):
		return self.score <= other.score
	
	def __gt__(self, other):
		return self.score > other.score
	
	def __ge__(self, other):
		return self.score >= other.score

	@staticmethod
	def random(n=7):
		"""randomly generate a poker hand from #n of non-repeat cards
		"""
		if n > 26:
			print("Warning, picking the best pokerhand from more than 26 cards is slow.")
			
		h = Hands.random(n=n, non_repeat=True)
		pokerhand = None
		for cards in itertools.combinations(h, 5):
			p = PokerHand(Hands(list(cards)))
			try:
				if pokerhand <= p:
					pokerhand = p
			except:
				pokerhand = p
		return pokerhand

	
	
if __name__ == "__main__":
	import unittest
	import time

# 	h = Hands.random(5)
# 	print(h.icon())
# 	p = PokerHand(h)
# 	print(p)

	p = PokerHand.random(7)
	print(p)

	def hash_speed_test():
		h = Hands.random(5)

		st = time.clock()
		for _ in range(1000):
			h.sign()
		print("sign method elaspe: ", time.clock() - st)
		
		st = time.clock()
		for _ in range(1000):
			h.hash()
		print("sign method elaspe: ", time.clock() - st)

		st = time.clock()
		for _ in range(1000):
			h.bitmap()
		print("bitmap method elaspe: ", time.clock() - st)

# 	hash_speed_test()

	def hash_performance_test():
		deck = Deck()
		
		s = set()
		st = time.clock()
		for cards in itertools.combinations(deck, 5):
			s.add( Hands(list(cards)).sign() )
		print(time.clock() - st)
		print(len(s)) # 2598960
		
		s = set()
		st = time.clock()
		for cards in itertools.combinations(deck, 5):
			s.add( Hands(list(cards)).hash() )
		print(time.clock() - st)
		print(len(s)) # 2598960
		
# 	hash_performance_test()

	def comparison_test():
		p1 = PokerHand.random(10)
		p2 = PokerHand.random(10)
		if p1.score > p2.score:
			print("%s - [%s] win %s - [%s]" % (p1.icon(), p1.pattern, p2.icon(), p2.pattern))
		elif p1.score < p2.score:
			print("%s - [%s] win %s - [%s]" % (p2.icon(), p2.pattern, p1.icon(), p1.pattern))
		else:
			print("%s - [%s] draw %s - [%s]" % (p1.icon(), p1.pattern, p2.icon(), p2.pattern))
		
# 	comparison_test()
	
# 	st = time.clock()
# 	p = PokerHand.random(n=7)
# 	print(p.icon(), p.pattern)
# 	print(time.clock() - st)
	
	def poker():
		h = Hands.random(7)
		print(h.icon())
		print(h.pick_best_pokerhand())
# 	poker()

	class PokerHandUnittest(unittest.TestCase):
		def test_detector(self):
			ROYALFLUSH = PokerHand(Hands([
								Card(suit=1, rank=10), 
								Card(suit=1, rank=11), 
								Card(suit=1, rank=12), 
								Card(suit=1, rank=13), 
								Card(suit=1, rank=14),
								]))
			self.assertEqual(ROYALFLUSH.pattern, "ROYAL FLUSH")
			self.assertEqual(ROYALFLUSH.score, 10*14**5)
			
			ROYALFLUSH = PokerHand(Hands([
								Card(suit=4, rank=10), 
								Card(suit=4, rank=11), 
								Card(suit=4, rank=12), 
								Card(suit=4, rank=13), 
								Card(suit=4, rank=1),
								]))
			self.assertEqual(ROYALFLUSH.pattern, "ROYAL FLUSH")
			self.assertEqual(ROYALFLUSH.score, 10*14**5)
			
			STRAIGHTFLUSH = PokerHand(Hands([
								Card(suit=1, rank=1), 
								Card(suit=1, rank=2), 
								Card(suit=1, rank=3), 
								Card(suit=1, rank=4), 
								Card(suit=1, rank=5),
								]))
			self.assertEqual(STRAIGHTFLUSH.pattern, "STRAIGHT FLUSH")
			self.assertEqual(STRAIGHTFLUSH.score, 9*14**5 + 1*14**4)
			
			STRAIGHTFLUSH = PokerHand(Hands([
								Card(suit=2, rank=14), 
								Card(suit=2, rank=2), 
								Card(suit=2, rank=3), 
								Card(suit=2, rank=4), 
								Card(suit=2, rank=5),
								]))
			self.assertEqual(STRAIGHTFLUSH.pattern, "STRAIGHT FLUSH")
			self.assertEqual(STRAIGHTFLUSH.score, 9*14**5 + 1*14**4)
			
			STRAIGHTFLUSH = PokerHand(Hands([
								Card(suit=3, rank=5), 
								Card(suit=3, rank=6), 
								Card(suit=3, rank=7), 
								Card(suit=3, rank=8), 
								Card(suit=3, rank=9),
								]))
			self.assertEqual(STRAIGHTFLUSH.pattern, "STRAIGHT FLUSH")
			self.assertEqual(STRAIGHTFLUSH.score, 9*14**5 + 5*14**4)
			
			FLUSH = PokerHand(Hands([
							Card(suit=1, rank=2), 
							Card(suit=1, rank=4), 
							Card(suit=1, rank=7), 
							Card(suit=1, rank=8), 
							Card(suit=1, rank=11),
							]))
			self.assertEqual(FLUSH.pattern, "FLUSH")
			self.assertEqual(FLUSH.score, 6*14**5 + 11*14**4 + 8*14**3 + 7*14**2 + 4*14 + 2)
			
			STRAIGHT = PokerHand(Hands([
							Card(suit=1, rank=5), 
							Card(suit=2, rank=6), 
							Card(suit=3, rank=7), 
							Card(suit=4, rank=8), 
							Card(suit=1, rank=9),
							]))
			self.assertEqual(STRAIGHT.pattern, "STRAIGHT")
			self.assertEqual(STRAIGHT.score, 5*14**5 + 5*14**4)
			
			STRAIGHT = PokerHand(Hands([
							Card(suit=1, rank=14), 
							Card(suit=2, rank=2), 
							Card(suit=3, rank=3), 
							Card(suit=4, rank=4), 
							Card(suit=1, rank=5),
							]))
			self.assertEqual(STRAIGHT.pattern, "STRAIGHT")
			self.assertEqual(STRAIGHT.score, 5*14**5 + 1*14**4)
			
			STRAIGHT = PokerHand(Hands([
							Card(suit=1, rank=10), 
							Card(suit=2, rank=11), 
							Card(suit=3, rank=12), 
							Card(suit=4, rank=13), 
							Card(suit=1, rank=1),
							]))
			self.assertEqual(STRAIGHT.pattern, "STRAIGHT")
			self.assertEqual(STRAIGHT.score, 5*14**5 + 10*14**4)

			FourOfKind = PokerHand(Hands([
							Card(suit=1, rank=1), 
							Card(suit=2, rank=1), 
							Card(suit=3, rank=1), 
							Card(suit=4, rank=1), 
							Card(suit=1, rank=2),
							]))
			self.assertEqual(FourOfKind.pattern, "4 OF A KIND")
			self.assertEqual(FourOfKind.score, 8*14**5 + 14*14**4 + 2*14**3)

			FullHouse = PokerHand(Hands([
							Card(suit=1, rank=1), 
							Card(suit=2, rank=1), 
							Card(suit=3, rank=1), 
							Card(suit=1, rank=2), 
							Card(suit=2, rank=2),
							]))
			self.assertEqual(FullHouse.pattern, "FULL HOUSE")
			self.assertEqual(FullHouse.score, 7*14**5 + 14*14**4 + 2*14**3)
			
			ThreeOfKind = PokerHand(Hands([
					Card(suit=1, rank=1), 
					Card(suit=2, rank=1), 
					Card(suit=3, rank=1), 
					Card(suit=1, rank=2), 
					Card(suit=1, rank=3),
					]))
			self.assertEqual(ThreeOfKind.pattern, "3 OF A KIND")
			self.assertEqual(ThreeOfKind.score, 4*14**5 + 14*14**4 + 3*14**3 + 2*14**2)
			
			TwoPair = PokerHand(Hands([
						Card(suit=1, rank=1), 
						Card(suit=2, rank=1), 
						Card(suit=1, rank=2), 
						Card(suit=2, rank=2), 
						Card(suit=1, rank=3),
						]))
			self.assertEqual(TwoPair.pattern, "2 PAIR")
			self.assertEqual(TwoPair.score, 3*14**5 + 14*14**4 + 2*14**3 + 3*14**2)
			
			OnePair = PokerHand(Hands([
						Card(suit=1, rank=1), 
						Card(suit=2, rank=1), 
						Card(suit=1, rank=2), 
						Card(suit=1, rank=3), 
						Card(suit=1, rank=4),
						]))
			self.assertEqual(OnePair.pattern, "1 PAIR")
			self.assertEqual(OnePair.score, 2*14**5 + 14*14**4 + 4*14**3 + 3*14**2 + 2*14)
			
			HighCard = PokerHand(Hands([
						Card(suit=1, rank=1), 
						Card(suit=2, rank=3), 
						Card(suit=3, rank=5), 
						Card(suit=4, rank=7), 
						Card(suit=1, rank=9),
						]))
			self.assertEqual(HighCard.pattern, "HIGH CARD")
			self.assertEqual(HighCard.score, 1*14**5 + 14*14**4 + 9*14**3 + 7*14**2 + 5*14 + 3)
		
		
	class CardUnittest(unittest.TestCase):
		def test_initialize(self):
			"""
			"""
			c = Card(suit=1, rank=1)
			self.assertEqual(str(c), "Ace of Spade")
			self.assertEqual(repr(c), "Card(suit=1, rank=14)")
			
			with self.assertRaises(InvalidCardError):
				c = Card(suit=0, rank=1)

			with self.assertRaises(InvalidCardError):
				c = Card(suit=1, rank=0)
		
		def test_hash(self):
			self.assertEqual(hash(Card(suit=1, rank=1)), 14*4+1)
			self.assertEqual(hash(Card(suit=1, rank=14)), 14*4+1)
		
		def test_operator(self):
			self.assertTrue(Card(suit=1, rank=1) == Card(suit=1, rank=1))
			self.assertFalse(Card(suit=1, rank=1) == Card(suit=1, rank=13))
			
			self.assertGreater(Card(suit=1, rank=6), Card(suit=1, rank=5))
			self.assertGreater(Card(suit=4, rank=10), Card(suit=1, rank=10))
			self.assertGreater(Card(suit=1, rank=1), Card(suit=4, rank=13))
			
	class HandsUnittest(unittest.TestCase):
		def test_initialize(self):
			h = Hands(cards=[
					Card(suit=1, rank=1),
					Card(suit=2, rank=2),
					])
			self.assertEqual(str(h), "1. Ace of Spade\n2. Two of Heart")
			self.assertEqual(repr(h), "Hands(cards=[Card(suit=1, rank=14), Card(suit=2, rank=2)])")

		def test_random(self):
			h = Hands.random(n=7, non_repeat=True)
			self.assertEqual(len(h), 7)

		def test_shuffle(self):
			h = Hands.random(n=7, non_repeat=True)
			string_before = str(h)
			h.shuffle()
			string_after = str(h)
			self.assertNotEqual(string_before, string_after)
		
		def test_sort(self):
			h = Hands.random(n=7, non_repeat=True)
			h.sort()

		def test_list(self):
			h = Hands.random(n=5, non_repeat=True)
			print(list(h))
			print(set(h))

		def test_pick_best_pokerhand(self):
			h = Hands(cards=[
					Card(suit=1, rank=1),
					Card(suit=2, rank=1),
					Card(suit=3, rank=1),
					Card(suit=1, rank=10),
					Card(suit=2, rank=10),
					Card(suit=3, rank=2),
					Card(suit=4, rank=13),
					])
			p = h.pick_best_pokerhand()
			self.assertEqual(p.pattern, "FULL HOUSE")
			self.assertEqual(p.score, 4330032)
			
			
	class DeckUnittest(unittest.TestCase):
		def test_initialize(self):
			d = Deck(n=1, shuffle=True)
			self.assertEqual(len(d), 52)

		def test_dealing(self):
			d = Deck(n=1, shuffle=False)
			h = Hands()
			h.add_card(d.deal_card())
			self.assertEqual(h[0], Card(suit=1, rank=1))

			h.add_hands(d.deal_hands(3))
			self.assertEqual(h[3], Card(suit=1, rank=4))
			
# 	unittest.main()
	
