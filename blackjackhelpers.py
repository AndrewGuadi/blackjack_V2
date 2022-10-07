import abc, itertools, random, time
from enum import Enum
from dataclasses import dataclass



class User(metaclass=abc.ABCMeta):

    def __init__(self):

        self.name = ""
        self.score = 0
        self.hand = []
        self.balance = 0

    @abc.abstractmethod
    def define_name(self):
        """Set either the dealer or player name"""
        return

    def print_hand(self, cards_to_be_shown):
        if cards_to_be_shown > len(self.hand):
            print("Too many cards requested to be shown")
            return

        counter = 0
        print(f"\n\n{self.name}'s HAND:")
        for card in self.hand:
            print(card)
            counter += 1
            if counter >= cards_to_be_shown:
                print('', end="\r")
                break

    def discard_hand(self):
        self.hand = []


    def calculate_score(self):
        self.score = 0
        for card in self.hand:
            self.score += card.rank.points

    def print_score(self):
        print(f"Total Score: {self.score}")   

    def add_card_to_hand(self, card):
        self.hand.append(card)

    

class Player(User):

    def __init__(self):
        super(Player, self).__init__()
        self.balance = 200
        self.define_name()
        self.bet = self.place_bet()
        

    def define_name(self):

        while True:

            user_name = input("Your Name:  ")
            confirmation = input(f"Your name is {user_name}? Y/N: ")
            confirmation = confirmation.lower().strip()

            if confirmation == "y":
                self.name = user_name
                print("username set!")
                break
    
    def place_bet(self):

        while True:
            response = input(f"BALANCE: {self.balance}\nMake Bet (1/2/5/10/25/50/100): ")

            try:
                current_bet = int(response)
            except ValueError:
                print("Please Enter a Valid number")

            else: 
                if current_bet not in (1, 2, 5, 10, 25, 50,100, 1000):
                    print("Sorry, only bets of exactly 1, 2, 5, 10, 25, 50 & 100 are allowed.")
                else:
                    if current_bet <= self.balance:
                        self.balance -= current_bet
                        self.bet = current_bet
                        print(f"${self.bet} BET PLACED")
                        break
                    else:
                        print(f"Amount Entered Higher than Balance. MAXIMUM BET = {self.balance}")

    def reset_bet(self):
        self.bet = 0
    
    def get_user_action(self):
        likely_action = ''

        while True:
            actions = ("hit", "stand")
            response = input("HIT OR STAND?:  ")
            response = response.lower().strip()

            counter = 0
            for i in range(len(response)):
                try:
                    if response[i] == actions[0][i]:
                        counter += 1
                        likely_action = actions[0]
                    elif response[i] == actions[1][i]:
                        counter += 1
                        likely_action = actions[1]
                except:
                    "just keep swimming. I feel like its bad practice but I used the try loop "
            
            if counter < 2:
                print("Please Re-enter: ")
            else:
                ##print(f"Youve Entered {likely_action}")
                return likely_action
                break

        






    #What can a player do that a dealer cannot?
    #makebet

class Dealer(User):

    def __init__(self):
        super(Dealer, self).__init__()
        self.balance = 1000000
        self.define_name()

    def define_name(self):
        self.name = "Dealer"
    
    #what can a dealer do that a player cannot?
    #show one card on deal

class Rank(Enum):
    TWO = ('2', 2)
    THREE = ('3', 3)
    FOUR = ('4', 4)
    FIVE = ('5', 5)
    SIX = ('6', 6)
    SEVEN = ('7', 7)
    EIGHT = ('8', 8)
    NINE = ('9', 9)
    TEN = ('10', 10)
    JACK = ('J', 10)
    QUEEN = ('Q', 10)
    KING = ('K', 10)
    ACE = ('A', 11)

    @property
    def symbol(self):
        return self.value[0]

    @property
    def points(self):
        return self.value[1]



class Suits(Enum):
    CLUBS = ('Clubs', '♣')
    DIAMONDS = ('Diamonds', '♦')
    HEART = ('Hearts', '♥')
    SPADES = ('Spades', '♠')

    @property
    def suit_name(self):
        return self.value[0]

    @property
    def symbol(self):
        return self.value[1]


@dataclass(frozen=True)
class Card:
    rank: Rank
    suit: Suits

    def point_value(self):
        return self.rank.points

    def __str__(self):
        return f"{self.rank.symbol} of {self.suit.suit_name} {self.suit.symbol}"
        


class Deck:
    def __init__(self):
        self.deck = [Card(rank, suit) for rank, suit in itertools.product(Rank, Suits)]

        random.shuffle(self.deck)


    def reveal_deck(self):
        
        for card in self.deck:
            card = str(card)
            print(card)



class Shoe:

    def __init__(self):

        self.new_shoe = []
        for i in range(5):
            for card in Deck().deck:
                self.new_shoe.append(card)
                      
    def reveal_shoe(self):

        print(self.new_shoe)

    def deal_one_card(self):
        card_dealt = self.new_shoe[0]
        self.new_shoe.pop(0)
        return card_dealt


class Game:

    def __init__(self, player, dealer, shoe):
        self.player = player
        self.dealer = dealer
        self.game_shoe = shoe


    def deal_cards(self, cards_per_player):

        for i in range(cards_per_player):
            self.player.add_card_to_hand(self.game_shoe.deal_one_card())
            self.dealer.add_card_to_hand(self.game_shoe.deal_one_card())

        ###delete this (prints out the current hand data)
        ###print(self.player.hand)
        ###print(self.dealer.hand)


    def hit(self, person):
      
        person.add_card_to_hand(self.game_shoe.deal_one_card())
        person.calculate_score()
        person.print_hand(len(person.hand))
        person.print_score()
            
        

    def stand(self):
        print(f"Chose to stay")
        
        

    def play_action(self, action, person):
        if action == "hit":
            self.hit(person)
        elif action == "stand":
            self.stand()
        else:
            ("Somehow a bad action was passed")

    def player_turn(self):

        while True:
            action = self.player.get_user_action()
            self.play_action(action, self.player)
            if action == "stand":
                break
            elif self.player.score > 21:
                print("Ya busted early bud\nGAME OVER")
                self.player.reset_bet()
                self.reset_hands()
                self.keep_playing()
                break

    def dealer_turn(self):
        self.dealer.print_hand(len(self.dealer.hand))
        self.dealer.print_score()

        while True:
            self.dealer.calculate_score()
            if self.dealer.score < 16:
                self.play_action("hit", self.dealer)

            elif self.dealer.score >= 16 and self.dealer.score < 22:
                self.play_action("stand", self.dealer)
                break

            elif self.dealer.score >= 22:
                print("Dealer BUSTS!")
                self.payout()
                self.player.reset_bet()
                self.reset_hands()
                self.keep_playing()
                break

    def reset_hands(self):
        self.player.discard_hand()
        self.dealer.discard_hand()
    

    def payout(self):
        print(self.player.bet)
        self.dealer.balance -= self.player.bet
        self.player.balance += (self.player.bet * 2)


    def game_begin(self):
        if self.player.bet == 0:
            self.player.place_bet()
        self.deal_cards(2)
        self.player.print_hand(2)
        self.player.calculate_score()
        self.player.print_score()
        self.dealer.print_hand(1)
        self.dealer.calculate_score()

    def middle_game(self):
        self.player_turn()
        if self.player.score < 22:
            self.dealer_turn()
            if self.dealer.score < 22:
                self.end_game()
            else:
                ##ask next game function
                pass

    def end_game(self):
        
        if self.player.score > self.dealer.score:
            print("YOU WIN!")
            self.payout()
            #payout to player
            pass
        elif self.player.score >= self.dealer.score:
            print("DEALER WINS!!")
        self.reset_hands()
        self.player.reset_bet()
        keep_playing_variable = self.keep_playing()
        ##determine winner
        #payout winner
        #reset_bet()
        #ask next game function
        return keep_playing_variable

    def keep_playing(self):
        
        response = input("Would you like to keep playing? Y/N: ")
        response = response.lower().strip()

        if response == "n":
            return False
