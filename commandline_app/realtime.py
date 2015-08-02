##encoding=utf-8

from royalflush.database import client, score, seven_cards_score
from royalflush.cards import Card, _CARD_CODES, Hands, Deck, PokerHand
import itertools
import pymongo
from angora.DATA.pk import load_pk, safe_dump_pk
import time

score_dict = load_pk("score_dict.pickle")
seven_cards_score_dict = dict()
for filename in ["seven_cards_score_%s.pickle" % i for i in range(1, 14+1)]:
    for k, v in load_pk(filename).items():
        seven_cards_score_dict[k] = v

################
# 算牌辅助函数 #
################

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

def find_one_enemy_lose_odd(board_5_cards, rest_45_cards, my_score):
    """计算对于一个敌人而言, 有多大的可能性在桌面上已有5张牌, 而我手中有
    2张牌的情况下, 我会输。
    """
    # 计算有多少种两张牌的可能性会超过我
    counter = 0
    for two_cards in itertools.combinations(rest_45_cards, 2):
        enemy_all = board_5_cards + list(two_cards)
        
        # 计算敌人手牌的分值
        enemy_score = 0
        for enemy_pokerhand in itertools.combinations(enemy_all, 5):
            
            # 计算敌人手牌的bitmap
            bitmap = 0
            for card in enemy_pokerhand:
                bitmap |= (1 << (hash(card) - 1))
                
            current_score = score_dict[bitmap]
            if enemy_score < current_score:
                enemy_score = current_score
        
        if enemy_score > my_score:
            counter += 1
    
    lose_odd = counter/990
    win_odd = 1 - lose_odd
    return win_odd, lose_odd, counter

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

################
# 模拟玩牌函数 #
################
def flop():
    """模拟发3张公牌
    """
    deck = Deck()
    board = deck.deal_hands(3)
    myhand = deck.deal_hands(2)
    return myhand, board, deck

def turn():
    """模拟发4张公牌
    """
    deck = Deck()
    board = deck.deal_hands(4)
    myhand = deck.deal_hands(2)
    return myhand, board, deck

def river():
    """模拟发5张公牌
    """
    deck = Deck()
    board = deck.deal_hands(5)
    myhand = deck.deal_hands(2)
    return myhand, board, deck

def river_round_cache():
    """模拟river轮的概率计算
    """
    number_of_players = 5
#     myhand, board, deck = river()
    
    # 测试用
    board = Hands(cards=[Card(suit=4, rank=13), Card(suit=2, rank=10), Card(suit=1, rank=7), Card(suit=3, rank=8), Card(suit=1, rank=2)])
    myhand = Hands(cards=[Card(suit=3, rank=5), Card(suit=2, rank=7)])
    deck = Hands(list(set(Deck().cards).difference( set(board.cards + myhand.cards) ) ) )
    
    
    st = time.clock()
    
    my_score = find_best_score_cache(myhand.cards + board.cards) # 计算我的手牌分数
    
    win_odd, lose_odd, counter = find_one_enemy_lose_odd_cache(
        board.cards, deck.cards, my_score)
    
    odd = list()
    for i in range(1, number_of_players):
        odd.append((i, "%.4f" % (1 - win_odd ** i,)))
    
    print("\n")
    print("board = %s, %s" % (board.icon(), board.cards) )
    print("myhand = %s, %s" % (myhand.icon(), myhand.cards) )
    print("my_score = %s" % my_score)
    print("threaten posibility = %s" % counter)
    print("lose_odd = %s" % odd)
    print("elapse %.6f sec" % (time.clock() - st,))

# river_round_cache()

def turn_round_cache():
    """模拟turn轮的概率计算
    """
    number_of_players = 5
    myhand, board, deck = turn()
    
    st = time.clock()
    
    _win_odd = 0
    for card in deck.cards:
        new_board_cards = board.cards + [card]
        new_deck_cards = list(deck.cards)
        new_deck_cards.remove(card)
        
        my_score = find_best_score_cache(myhand.cards + new_board_cards)

        win_odd, lose_odd, counter = find_one_enemy_lose_odd_cache(
            new_board_cards, new_deck_cards, my_score)
        _win_odd += win_odd
    
    _win_odd /= 46
    
    odd = list()
    for i in range(1, number_of_players):
        odd.append((i, "%.4f" % (1 - _win_odd ** i,)))

    print("\n")
    print("board = %s, %s" % (board.icon(), board.cards) )
    print("myhand = %s, %s" % (myhand.icon(), myhand.cards) )
    print("my_score = %s" % my_score)
    print("threaten posibility = %s" % counter)
    print("lose_odd = %s" % odd)
    print("elapse %.6f sec" % (time.clock() - st,))

def flop_round_cache():
    """模拟flop轮的概率计算
    """
    number_of_players = 5
    myhand, board, deck = flop()
    
    st = time.clock()
    
    _win_odd = 0
    for two_cards in itertools.combinations(deck.cards, 2):
        new_board_cards = board.cards + list(two_cards)
        new_deck_cards = list(deck.cards) # 从牌堆中移除两张给对手的牌
        new_deck_cards.remove(two_cards[0])
        new_deck_cards.remove(two_cards[1])
        
        my_score = find_best_score_cache(myhand.cards + new_board_cards) # 计算我的手牌分数

        win_odd, lose_odd, counter = find_one_enemy_lose_odd_cache(
            new_board_cards, new_deck_cards, my_score)
        _win_odd += win_odd
    
    _win_odd /= 1081
    
    odd = list()
    for i in range(1, number_of_players):
        odd.append((i, "%.4f" % (1 - _win_odd ** i,)))

    print("\n")
    print("board = %s, %s" % (board.icon(), board.cards) )
    print("myhand = %s, %s" % (myhand.icon(), myhand.cards) )
    print("my_score = %s" % my_score)
    print("threaten posibility = %s" % counter)
    print("lose_odd = %s" % odd)
    print("elapse %.6f sec" % (time.clock() - st,))


if __name__ == "__main__":
    

    
    def river_round():
        number_of_players = 5
#         myhand, board, deck = river()
        
        # 测试用
        board = Hands(cards=[Card(suit=4, rank=13), Card(suit=2, rank=10), Card(suit=1, rank=7), Card(suit=3, rank=8), Card(suit=1, rank=2)])
        myhand = Hands(cards=[Card(suit=3, rank=5), Card(suit=2, rank=7)])
        deck = Hands(list(set(Deck().cards).difference( set(board.cards + myhand.cards) ) ) )
        
        my_score, my_pockerhand = find_best_score(myhand.cards + board.cards)
        st = time.clock()
        win_odd, lose_odd, counter = find_one_enemy_lose_odd(
            board.cards, deck.cards, my_score)
        
        odd = list()
        for i in range(1, number_of_players):
            odd.append((i, "%.4f" % (1 - win_odd ** i,)))
        
        print("\n")
        print("board = %s, %s" % (board.icon(), board.cards))
        print("myhand = %s, %s" % (myhand.icon(), myhand.cards))
        print("my_pokerhand = %s, my_score = %s" % (Hands(list(my_pockerhand)).icon(), my_score  )  )
        print("threaten posibility = %s" % counter)
        print("lose_odd = %s" % odd)
        print("elapse %.6f sec" % (time.clock() - st,))
    
    def turn_round():
        number_of_players = 5
        myhand, board, deck = turn()
        
        _win_odd = 0
        
        st = time.clock()
        
        for card in deck.cards:
            new_board_cards = board.cards + [card]
            new_deck_cards = list(deck.cards)
            new_deck_cards.remove(card)
            
            my_score, my_pockerhand = find_best_score(myhand.cards + new_board_cards)

            win_odd, lose_odd, counter = find_one_enemy_lose_odd(
                new_board_cards, new_deck_cards, my_score)
            _win_odd += win_odd
        
        _win_odd /= 46
        
        odd = list()
        for i in range(1, number_of_players):
            odd.append((i, "%.4f" % (1 - _win_odd ** i,)))

        print("\n")
        print("board = %s, %s" % (board.icon(), board.cards))
        print("myhand = %s, %s" % (myhand.icon(), myhand.cards))
        print("my_pokerhand = %s, my_score = %s" % (Hands(list(my_pockerhand)).icon(), my_score  )  )
        print("threaten posibility = %s" % counter)
        print("lose_odd = %s" % odd)
        print("elapse %.6f sec" % (time.clock() - st,))
        

    while 1:
#         river_round()
#         river_round_cache()
        turn_round_cache()
#         flop_round_cache()
        input("press any key to continue...")