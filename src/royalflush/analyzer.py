##encoding=utf-8

from royalflush.cards import Card, Hands, Deck, PokerHand


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
    me = Me()
    game = Game(6, me)
    board = game.board
     
    # === playing ===
    game.blind()
    print("me:", me.icon())

    game.preflop()
    print("board:", board.icon())
 
    game.turn()
    print("board:", board.icon())
    
    game.river()
    print("board:", board.icon())
#     me = Me()
#     board = Board()
#     me.cards.append(1)
#     print(me.cards)
#     print(board.cards)
# #     me.add_hands(Hands.random(1))
# #     print(me, board)