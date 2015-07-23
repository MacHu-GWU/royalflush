##encoding=utf-8

from royalflush.cards import Card, _CARD_CODES, Hands, Deck, PokerHand
from royalflush.database import client, score
from royalflush.bitmath import create_bitmap
from angora.DATA import *
import itertools

class Board(Hands):
    pass

class Me(Hands):
    pass

class Game():
    def __init__(self, num_of_players, me):
        self.total_players = num_of_players
        self.n_on_table = num_of_players
        self.n_out = 0
        
        self.deck = Deck()
        self.undealed = Deck()
        
        self.board = Board()
        
        self.me = me
        
    def blind(self):
        self.me.add_hands(self.deck.deal_hands(2))
        for _ in range(self.total_players-1):
            self.deck.deal_hands(2)
    
    def preflop(self):
        self.board.add_hands(self.deck.deal_hands(3))
    
    def turn(self):
        self.board.add_hands(self.deck.deal_hands(1))
        
    def river(self):
        self.board.add_hands(self.deck.deal_hands(1))
        # === 计算概率 ===
        
        
        
if __name__ == "__main__":
    from angora.GADGET import Timer
    _score = load_pk("score_dict.pickle")
    
#     @profile
    def test1():
    #     _score = dict()
    #     for doc in score.find():
    #         _score[doc["_id"]] = doc["score"]
    #     safe_dump_pk(_score, "score.pickle")
        
        
        timer = Timer()
        
        me = Me()
        game = Game(6, me)
        board = game.board
         
        # === playing ===
        game.blind()
    #     print("me:", me.icon())
    
        game.preflop()
    #     print("board:", board.icon())
     
        game.turn()
    #     print("board:", board.icon())
        
        game.river()
    #     print("board:", board.icon())
        
        me.add_hands(board)
        
        my_pokerhand = me.pick_best_pokerhand()
        board_set = set(board)
    #     print(board_set)
    #     timer.start()
    #     counter = 0
    #     for doc in score.find({"score": {"$gt": my_pokerhand.score}}):
    #         threaten_hand = {_CARD_CODES[int(i)] for i in doc["_id"].split("-")}
    #         if len(threaten_hand.difference(board_set)) <= 2:
    #             counter += 1
    #     timer.timeup()
    #     print(counter)
    
        timer.start()
        counter1 = 0
        counter2 = 0
        for cards in itertools.combinations(game.deck, 2):
            
    #         enemy_value = 0
    #         seven_cards = list(board.cards) + list(cards)
    #         for five_cards in itertools.combinations(seven_cards, 5):
    #             five_cards = list(five_cards)
    #             five_cards.sort()
    #             _id = "-".join([str(hash(card)) for card in five_cards])
    #             value = score.find_one({"_id": _id})["score"]
    #             if enemy_value < value:
    #                 enemy_value = value
    #             
    #         if enemy_value > my_pokerhand.score:
    #             counter1 += 1
    
            enemy_value = 0
            seven_cards = list(board.cards) + list(cards)
            for five_cards in itertools.combinations(seven_cards, 5):
     
                value = 0
                for card in five_cards:
                    value |= (1 << (hash(card) - 1))
#                     value += 1 << (hash(card) - 1)
                
                now_score = _score[value]
                if enemy_value < now_score:
                    enemy_value = now_score
                    
            if enemy_value > my_pokerhand.score:
                counter1 += 1
    
    
    #         p = Hands(list(board.cards) + list(cards)).pick_best_pokerhand()
    #         p.cards.sort()
    #         sign = "-".join([str(hash(card)) for card in p.cards])
    #         doc = score.find_one({"_id": sign})
    #         if doc["score"] > my_pokerhand.score:
    #             counter2 += 1
    
    #         p = Hands(list(board.cards) + list(cards)).pick_best_pokerhand()
    #         p.cards.sort()
    #          
    #         value = 0
    #         for card in p.cards:
    #             value += 1 << (hash(card) - 1)
    #          
    #         if _score[value] > my_pokerhand.score:
    #             counter2 += 1
                
    #         doc = score.find_one({"_id": value})
    #         if doc["score"] > my_pokerhand.score:
    #             counter2 += 1
    
        print(counter1, counter2)
        timer.timeup()
    test1()
    
#     me = Me()
#     board = Board()
#     me.cards.append(1)
#     print(me.cards)
#     print(board.cards)
# #     me.add_hands(Hands.random(1))
# #     print(me, board)