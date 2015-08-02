#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
本脚本用于生成缓存数据
"""

from royalflush.database import client, five_cards_score, seven_cards_score
from royalflush.cards import Hands, Deck, PokerHand
from royalflush.pk import load_pk, safe_dump_pk
import itertools
import pymongo
import time

####################
# five cards score #
####################

def calculate_five_cards_score_collection():
    """计算每一种5张牌的牌型的bitmap-key: score分值, 分值越大的牌就越大。
    将结果保存在score文档集中。最后将score文档集中的数据读取出来, 保存为pickle。
    然后之后将其加载入内存, 提高查询速度。
    """
#     five_cards_score.drop() # WARANING
    
    data = list()
     
    deck = Deck()
    for cards in itertools.combinations(deck, 5):
        h = Hands(list(cards))
        h.sort()
        p = PokerHand(h)
         
        doc = {"_id": h.bitmap(), "score": p.score}
        data.append(doc)
         
    five_cards_score.insert(data)
    five_cards_score.create_index([("score", pymongo.ASCENDING)])
    
    score_dict = dict()
    for doc in five_cards_score.find():
        score_dict[doc["_id"]] = doc["score"]
    safe_dump_pk(score_dict, "score_dict.pickle")
    
# calculate_five_cards_score_collection()

def picklize_five_cards_score_collection():
    d = dict()
    for doc in five_cards_score.find():
        d[doc["_id"]] = doc["score"]
    safe_dump_pk(d, "five_cards_score.pickle", fastmode=False)

#####################
# seven cards score #
#####################

def calculate_seven_cards_score_collection():
    """计算每一种7张牌的牌型中最大的那个牌型的bitmap-key, 保存在
    seven_cards_score文档集中。
    """
#     seven_cards_score.drop() # WARNING

    five_cards_score_dict = load_pk("five_cards_score.pickle")
    
    st = time.clock()
    
    deck = Deck()
    data = list()
    
    counter = 0
    
    # 从整幅牌中随机选出7张牌
    for seven_cards in itertools.combinations(deck.cards, 7):
        # 计算7张牌的bitmap
        bitmap = 0
        for card in seven_cards:
            bitmap |= (1 << (hash(card) - 1))
        
        # 计算这7张牌中最大的5张牌, 以及其分数
        my_bitmap = 0 # 玩家当前7张牌中最强的5张牌的bitmap
        my_score = 0 # 玩家当前7张牌中最强的5张牌的分值
        my_5_cards = None # 玩家当前能组成的最强5张牌
        
        for five_cards in itertools.combinations(seven_cards, 5):
            this_bitmap = 0
            for card in five_cards:
                this_bitmap |= (1 << (hash(card) - 1))
            this_score = five_cards_score_dict[this_bitmap]
            
            if my_score < this_score:
                my_bitmap = this_bitmap
                my_score = this_score
                my_5_cards = five_cards
        
        doc = {"_id": bitmap, "best": my_bitmap}
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
    
# calculate_seven_cards_score_collection()

def picklize_seven_cards_score_collection():
    """将用于查询7张牌中最大牌型的seven_cards_score文档集保存为pickle。之后
    就可以加载到内存中, 用于快速的查询。
    """
    score_dict = load_pk("five_cards_score.pickle")
    
    data = dict()
    counter = 0
    series_number = 1
    for doc in seven_cards_score.find():
        data[doc["_id"]] = score_dict[doc["best"]]
        counter += 1
        print(counter)
        if counter == 6689228: # 分20个包
            safe_dump_pk(data, "seven_cards_score_%s.pickle" % series_number)
            counter = 0
            series_number += 1
            data.clear()
    safe_dump_pk(data, "seven_cards_score_%s.pickle" % series_number)
    
# picklize_seven_cards_score_collection()

###########################
# not useful at this time #
###########################

def flop_round_odd_cache():
    score_dict = load_pk("score_dict.pickle")
    seven_cards_score_dict = dict()
    for filename in ["seven_cards_score_%s.pickle" % i for i in range(1, 14+1)]:
        for k, v in load_pk(filename).items():
            seven_cards_score_dict[k] = v

    def find_best_score(seven_cards):
        """计算七张牌能组成的最大牌型的分值
        """
        best_score = 0
    #     best_pokerhand = None
        for five_cards in itertools.combinations(seven_cards, 5):
            # 计算我手牌的bitmap
            bitmap = 0
            for card in five_cards:
                bitmap |= (1 << (hash(card) - 1))
    
            current_score = score_dict[bitmap]
            if best_score < current_score:
                best_score = current_score
    #             best_pokerhand = five_cards
        
        return best_score
    #     return best_score, best_pokerhand

    def find_best_score_cache(seven_cards):
        """计算七张牌能组成的最大牌型的分值。利用缓存, 速度快。
        """
        bitmap = 0
        for card in seven_cards:
            bitmap |= (1 << (hash(card) - 1))
        best_score = seven_cards_score_dict[bitmap]
        return best_score

    def find_one_enemy_lose_odd_cache(board_5_cards, rest_45_cards, my_score):
        """计算对于一个敌人而言, 有多大的可能性在桌面上已有5张牌, 而我手中有
        2张牌的情况下, 我会输。利用缓存, 速度快。
        """
        # 计算有多少种两张牌的可能性会超过我
        counter = 0
        for two_cards in itertools.combinations(rest_45_cards, 2):
            enemy_all = board_5_cards + list(two_cards)
            
            # 计算敌人手牌的分值
            enemy_score = find_best_score_cache(enemy_all)
            
            if enemy_score > my_score:
                counter += 1
        
        lose_odd = counter/990
        win_odd = 1 - lose_odd
        return win_odd, lose_odd, counter

    def flop_round_odd(my_two_cards, board_three_cards, deck_47_cards):
        """模拟flop轮的概率计算
        """
        _win_odd = 0
        # 从还没发的47张牌中选两张给公牌
        for two_cards in itertools.combinations(deck_47_cards, 2):
            # 此时公牌是5张牌
            new_board_cards = board_three_cards + list(two_cards)
            
            # 从剩余的47张牌中删去两张牌, 剩下45张未发的牌
            new_deck_cards = list(deck_47_cards)
            new_deck_cards.remove(two_cards[0])
            new_deck_cards.remove(two_cards[1])
            
            my_score = find_best_score_cache(my_two_cards + new_board_cards) # 计算我的手牌分数

            # 在5张公牌, 我有2张手牌的情况下, 计算一名敌人能击败你的概率
            win_odd, _, _ = find_one_enemy_lose_odd_cache(
                new_board_cards, new_deck_cards, my_score)
            _win_odd += win_odd
        
        _win_odd /= 1081
        return _win_odd
    
    
    deck = Deck()
    # 从整幅牌中选出5张牌
    counter = 0
    for five_cards in itertools.combinations(deck.cards, 5):
        counter += 1
        print(counter)
        
        bitmap = 0
        for card in five_cards:
            bitmap |= (1 << (hash(card) - 1))
        
        doc = {"_id": bitmap}
        
        # 从这5张牌中选出两张牌作为手牌
        for two_cards in itertools.combinations(five_cards, 2):
            bitmap = 0
            for card in two_cards:
                bitmap |= (1 << (hash(card) - 1))

            # 剩余的三张作为公牌
            three_cards = list(five_cards)
            three_cards.remove(two_cards[0])
            three_cards.remove(two_cards[1])
            
            # 从完整的52张牌中移除这5张牌, 剩下47张牌
            deck_cards = list(deck.cards)
            for card in five_cards:
                deck_cards.remove(card)

            _win_odd = flop_round_odd(list(two_cards), three_cards, deck_cards)
            
            doc[str(bitmap)] = _win_odd
        
        try:
            flop_odds.insert(doc)
        except:
            pass
        
# flop_round_odd_cache()

if __name__ == "__main__":
    print("complete")