#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
♠ A - 60		♥ A - 59		♣ A - 58		♦ A - 57
♠ K - 56		♥ K - 55		♣ K - 54		♦ K - 53
♠ Q - 52	♥ Q - 51	♣ Q - 50	♦ Q - 49
♠ J  - 48	♥ J  - 47	♣ J  - 46	♦ J  - 45
♠ 10 - 44	♥ 10 - 43	♣ 10 - 42	♦ 10 - 41
♠ 9 - 40		♥ 9 - 39		♣ 9 - 38		♦ 9 - 37
♠ 8 - 36		♥ 8 - 35		♣ 8 - 34		♦ 8 - 33
♠ 7 - 32		♥ 7 - 31		♣ 7 - 30		♦ 7 - 29
♠ 6 - 28		♥ 6 - 27		♣ 6 - 26		♦ 6 - 25
♠ 5 - 24		♥ 5 - 23		♣ 5 - 22		♦ 5 - 21
♠ 4 - 20		♥ 4 - 19		♣ 4 - 18		♦ 4 - 17
♠ 3 - 16		♥ 3 - 15		♣ 3 - 14		♦ 3 - 13
♠ 2 - 12		♥ 2 - 11		♣ 2 - 10		♦ 2 - 9
"""

class Glossary():
	def __init__(self):
		self.card_suit_alias = { # 花色的英文名
			1: "Spade",
			2: "Heart",
			3: "Clubs",
			4: "Diamond",
			}

		self.card_suit_icon_alias = { # 花色的图案
			1: "♦",
			2: "♣",
			3: "♥",
			4: "♠",
			}

		self.card_rank_alias = { # 牌面的英文名
			2: "Two",
			3: "Three",
			4: "Four",
			5: "Five",
			6: "Six",
			7: "Seven", 
			8: "Eight",
			9: "Nine",
			10: "Ten",
			11: "Jack",
			12: "Queen",
			13: "King",
			14: "Ace",
			}

		self.card_rank_icon_alias = { # 牌面的数字
			2: "2",
			3: "3",
			4: "4",
			5: "5",
			6: "6",
			7: "7", 
			8: "8",
			9: "9",
			10: "10",
			11: "J",
			12: "Q",
			13: "K",
			14: "A",
			}

		self.pokerhand_alias = { # 牌型的代码
			0: "UNKNOWN",
			1: "HIGH CARD",
			2: "1 PAIR",
			3: "2 PAIR",
			4: "3 OF A KIND",
			5: "STRAIGHT",
			6: "FLUSH",
			7: "FULL HOUSE",
			8: "4 OF A KIND",
			9: "STRAIGHT FLUSH",
			10: "ROYAL FLUSH"
			}

glossary = Glossary()

if __name__ == "__main__":
	pass