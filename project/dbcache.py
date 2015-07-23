##encoding=utf-8

from royalflush.database import client, score, seven_cards_score, odds, threaten
from royalflush.cards import Card, _CARD_CODES, Hands, Deck, PokerHand
import itertools
import pymongo
from angora.DATA.pk import load_pk, safe_dump_pk
import time

def calculate_bitmap_key_score_pair():
    """计算每一种牌型的bitmap-key: score分值, 分值越大的牌就越大
    """
    score.drop()
    data = list()
     
    deck = Deck()
    for cards in itertools.combinations(deck, 5):
        h = Hands(list(cards))
        h.sort()
        p = PokerHand(h)
         
        doc = {"_id": h.bitmap(), "score": p.score}
        data.append(doc)
         
    score.insert(data)
    score.create_index([("score", pymongo.ASCENDING)])
    
    score_dict = dict()
    for doc in score.find():
        score_dict[doc["_id"]] = doc["score"]
    safe_dump_pk(score_dict, "score_dict.pickle")
    
# calculate_bitmap_key_score_pair()

def calculate_bitmap_key_score_pair_for_seven_cards():
#     seven_cards_score.drop() # WARNING
    score_dict = load_pk("score_dict.pickle")
    deck = Deck()

    st = time.clock()
    data = list()
    
    counter = 0
    for seven_cards in itertools.combinations(deck.cards, 7):
        
        bitmap = 0
        for card in seven_cards:
            bitmap |= (1 << (hash(card) - 1))
        
        me_bitmap = 0 # 玩家当前7张牌中最强的5张牌的bitmap
        me_score = 0 # 玩家当前7张牌中最强的5张牌的分值
        me_5cards = None # 玩家当前能组成的最强5张牌
        for five_cards in itertools.combinations(seven_cards, 5):
            this_bitmap = 0
            for card in five_cards:
                this_bitmap |= (1 << (hash(card) - 1))
            this_score = score_dict[this_bitmap]
            
            if me_score < this_score:
                me_bitmap = this_bitmap
                me_score = this_score
                me_5cards = five_cards
        
        doc = {"_id": bitmap, "best": me_bitmap}
        data.append(doc)
        
        if len(data) == 10000:
            counter += len(data)
            try:
                seven_cards_score.insert(data)
            except:
                pass
            data.clear()
            print("now we have processed %s, %.2f%%" % (counter, counter*100/133784560))
        
    try:
        seven_cards_score.insert(data)
    except:
        pass
        
    print(time.clock() - st)
    
# calculate_bitmap_key_score_pair_for_seven_cards()

def seven_cards_score_to_pickle():
    data = dict()
    counter = 0
    series_number = 1
    for doc in seven_cards_score.find():
        data[doc["_id"]] = doc["best"]
        counter += 1
        print(counter)
        if counter == 30000000:
            safe_dump_pk(data, "seven_cards_score_%s.pickle" % series_number)
            counter = 0
            series_number += 1
            data.clear()
    safe_dump_pk(data, "seven_cards_score_%s.pickle" % series_number)
seven_cards_score_to_pickle()

def calculate_threaten_cards_number():
    score_dict = load_pk("score_dict.pickle")
    
    all_52_cards = set(_CARD_CODES.values())
    deck = Deck()

    for seven_cards in itertools.combinations(deck.cards, 7):
        seven_cards = (Card(suit=1, rank=10), Card(suit=4, rank=5), Card(suit=1, rank=13), Card(suit=2, rank=11), Card(suit=4, rank=7), Card(suit=2, rank=5), Card(suit=1, rank=7))
        
#         my_hand = Hands(list(seven_cards))
#         my_pokerhand = my_hand.pick_best_pokerhand()
#         print(my_hand)
#         print(my_pokerhand)
        
        bitmap = 0
        for card in seven_cards:
            bitmap |= (1 << (hash(card) - 1))
        my_score = score_dict[seven_cards_score.find_one({"_id": bitmap})["best"]]

        rest_45_cards = all_52_cards.difference(seven_cards)
        for five_cards_board in itertools.combinations(seven_cards, 5):
            st = time.clock()
            counter = 0
            for enemy_hand in itertools.combinations(rest_45_cards, 2):
                enemy = list(five_cards_board) + list(enemy_hand)
#                 print(Hands(enemy).icon())
                bitmap = 0
                for card in enemy:
                    bitmap |= (1 << (hash(card) - 1))
#                 enemy_score = score_dict[seven_cards_score.find_one({"_id": bitmap})["best"]]
                enemy_score = 1898652
                if enemy_score > my_score:
                    counter += 1
                    
            print(time.clock() - st)
            print(counter, my_score, seven_cards)
            return
# calculate_threaten_cards_number()

def test():
    score_dict = load_pk("score_dict.pickle")
    
    all_52_cards = set(_CARD_CODES.values())
    deck = Deck()

    for seven_cards in itertools.combinations(deck.cards, 7):
        seven_cards = (Card(suit=1, rank=10), Card(suit=4, rank=5), Card(suit=1, rank=13), Card(suit=2, rank=11), Card(suit=4, rank=7), Card(suit=2, rank=5), Card(suit=1, rank=7))
        
        bitmap = 0
        for card in seven_cards:
            bitmap |= (1 << (hash(card) - 1))
        my_score = score_dict[seven_cards_score.find_one({"_id": bitmap})["best"]]
        
        rest_45_cards = all_52_cards.difference(seven_cards)
        for five_cards_board in itertools.combinations(seven_cards, 5):
            st = time.clock()
            counter = 0
            for enemy_hand in itertools.combinations(rest_45_cards, 2):
                enemy = list(five_cards_board) + list(enemy_hand)
                
                enemy_score = 0
                for enemy_pokerhand in itertools.combinations(enemy, 5):
                    bitmap = 0
                    for card in enemy_pokerhand:
                        bitmap |= (1 << (hash(card) - 1))
                        
                    current_score = score_dict[bitmap]
                    if enemy_score < current_score:
                        enemy_score = current_score
                        
                if enemy_score > my_score:
                    counter += 1 
            
            print(time.clock() - st)
            print(counter, my_score, seven_cards)
            return
            
# test()
# print(seven_cards_score.find().count())
if __name__ == "__main__":
    print("complete")