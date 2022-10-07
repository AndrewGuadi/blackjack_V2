from blackjackhelpers import Player, Dealer, Deck, Shoe, Game

keep_playing_variable = True
player1 = Player()
dealer1 = Dealer()
game_shoe = Shoe()

new_game = Game(player1, dealer1, game_shoe)

while keep_playing_variable:
    new_game.game_begin()
    new_game.middle_game()
