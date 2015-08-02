##encoding=utf-8

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from royalflush.cards import _CARD_CODES, Deck
from metadata import seven_cards_score_dict
import itertools


################
# 算牌辅助函数 #
################
def find_best_pocker_hand_score_using_cache(seven_cards):
    """计算手中七张牌能组成的最大的牌型的分值。使用内存字典缓存。
    """
    bitmap = 0
    for card in seven_cards:
        bitmap |= (1 << (hash(card) - 1))
    best_score = seven_cards_score_dict[bitmap]
    return best_score

def find_lose_odd_if_one_enemy_using_cache(board_5_cards, rest_45_cards, my_score):
    """计算只有一个对手的情况下, 桌面上已有5张牌, 而我手中有2张牌的情况下, 
    有多大的概率, 我会输。使用内存字典缓存。
    """
    # 计算有多少种两张牌的可能性会超过我
    counter = 0
    for two_cards in itertools.combinations(rest_45_cards, 2):
        enemy_all = board_5_cards + list(two_cards)
        
        # 计算敌人手牌的分值
        enemy_score = find_best_pocker_hand_score_using_cache(enemy_all)
        
        if enemy_score > my_score:
            counter += 1
    
    lose_odd = counter/990
    win_odd = 1 - lose_odd
    return win_odd

################
# 游戏模拟函数 #
################
def river_round_solver(my_2_cards, board_5_cards, rest_45_cards):
    """模拟river轮的概率计算
    """
    number_of_players = 10
    my_score = find_best_pocker_hand_score_using_cache(my_2_cards + board_5_cards) # 计算我的手牌分数

    win_odd = find_lose_odd_if_one_enemy_using_cache(
                board_5_cards, rest_45_cards, my_score)
    
    odd = list()
    for i in range(1, number_of_players):
        odd.append((i, "%.4f" % (1 - win_odd ** i,)))
        
    return odd

def turn_round_solver(my_2_cards, board_4_cards, rest_46_cards):
    """模拟turn轮的概率计算
    """
    number_of_players = 10
    
    _win_odd = 0
    
    for card in rest_46_cards:
        new_board_cards = board_4_cards + [card] # 可能的5张公牌
        new_deck_cards = list(rest_46_cards) # 从牌堆中移除1张给对手的牌
        new_deck_cards.remove(card)
        
        my_score = find_best_pocker_hand_score_using_cache(my_2_cards + new_board_cards) # 计算我的手牌分数

        win_odd = find_lose_odd_if_one_enemy_using_cache(
                    new_board_cards, new_deck_cards, my_score)
        
        _win_odd += win_odd
    
    _win_odd /= 46
    
    odd = list()
    for i in range(1, number_of_players):
        odd.append((i, "%.4f" % (1 - _win_odd ** i,)))

    return odd

def flop_round_solver(my_2_cards, board_3_cards, rest_47_cards):
    """模拟flop轮的概率计算
    """
    number_of_players = 10
    
    _win_odd = 0
    
    for two_cards in itertools.combinations(rest_47_cards, 2):
        new_board_cards = board_3_cards + list(two_cards) # 可能的5张公牌
        new_deck_cards = list(rest_47_cards) # 从牌堆中移除2张给对手的牌
        new_deck_cards.remove(two_cards[0])
        new_deck_cards.remove(two_cards[1])
        
        my_score = find_best_pocker_hand_score_using_cache(my_2_cards + new_board_cards) # 计算我的手牌分数

        win_odd = find_lose_odd_if_one_enemy_using_cache(
                    new_board_cards, new_deck_cards, my_score)
        
        _win_odd += win_odd
    
    _win_odd /= 1081
    
    odd = list()
    for i in range(1, number_of_players):
        odd.append((i, "%.4f" % (1 - _win_odd ** i,)))

    return odd
    
def UserInput():
    while 1:
        arg1 = input("Input your cards: ")
        try:
            my_2_cards = [_CARD_CODES[int(s.strip())] for s in arg1.split(",")]
            if len(my_2_cards) != 2:
                raise Exception("my hand has to be exactly 2 cards!")
            if len(set(my_2_cards)) != 2:
                raise Exception("duplicate card error!")
            break
        except Exception as e:
            print(e)

    while 1:
        arg2 = input("Input board cards: ")
        try:
            board_cards = [_CARD_CODES[int(s.strip())] for s in arg2.split(",")]
            if len(board_cards) not in [3, 4, 5]:
                raise Exception("board card number error, has to be 3, 4, 5!")
            if len(set(board_cards)) != len(board_cards):
                raise Exception("duplicate card error!")
            if len(set.intersection(set(board_cards), set(my_2_cards))) != 0:
                raise Exception("my hands cannot have same cards in board!")
            break
        except Exception as e:
            print(e)
            
    return my_2_cards, board_cards

def main_loop():
    while 1:
        print("game start!")
        my_2_cards, board_cards = UserInput()
        rest_cards = Deck().cards
        for c in (my_2_cards + board_cards):
            rest_cards.remove(c)
    
        if len(board_cards) == 5:
            river_round_solver(my_2_cards, board_cards, rest_cards)
        elif len(board_cards) == 4:
            turn_round_solver(my_2_cards, board_cards, rest_cards)
        elif len(board_cards) == 3:
            flop_round_solver(my_2_cards, board_cards, rest_cards)
        else:
            print("wrong input, again.")

app = Flask("RoyalFlush")

def get_form_data(req):
    """get a copy of flask.request.form
    """
    d = dict()
    for key, value in req.form.items():
        if value:
            d.setdefault(key, value)
    return d

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        try:
        
            form = get_form_data(request)
            
            my_2_cards, board_cards = list(), list() 
            for k, v in form.items():
                card_code = int(k.split("_")[-1])
                option = int(v)
                if option == 1: # 手牌
                    my_2_cards.append(_CARD_CODES[card_code])
                elif option == 2:
                    board_cards.append(_CARD_CODES[card_code])
    
            rest_cards = Deck().cards
            for c in (my_2_cards + board_cards):
                rest_cards.remove(c)
            
            if len(board_cards) == 5:
                odd = river_round_solver(my_2_cards, board_cards, rest_cards)
            elif len(board_cards) == 4:
                odd = turn_round_solver(my_2_cards, board_cards, rest_cards)
            elif len(board_cards) == 3:
                odd = flop_round_solver(my_2_cards, board_cards, rest_cards)
    
            form["odd"] = str(odd)
    
            return render_template("index.html", **form)
        except:
            return render_template("index.html") 
    else:
        raise Exception()

@app.route("/reset", methods=["POST"])
def reset():
    return render_template("index.html")

@app.route("/<filename>", methods=["GET"])
def serve_static(filename):
    root = r"C:\HSH\Workspace\py33\py33_projects\royalflush\_statics"
    return send_from_directory(root, filename)

if __name__ == "__main__":
    app.run(host="localhost", port=12345, debug=True)