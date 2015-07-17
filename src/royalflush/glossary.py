##encoding=utf-8

class Glossary():
	def __init__(self):
		self.card_suit_alias = {
			1: "Spade",
			2: "Heart",
			3: "Clubs",
			4: "Diamond",
			}

		self.card_suit_icon_alias = {
			1: "♠",
			2: "♥",
			3: "♣",
			4: "♦",
			}

		self.card_rank_alias = {
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

		self.card_rank_icon_alias = {
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

		self.pokerhand_alias = {
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