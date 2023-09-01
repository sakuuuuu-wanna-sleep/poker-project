from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def make_row(im1, im2, im3, im4, im5):
    row = Image.new('RGB', (im1.width * 6, im1.height))
    row.paste(im1, (0, 0))
    row.paste(im2, (im1.width, 0))
    row.paste(im3, (im2.width*2, 0))
    row.paste(im4, (im3.width*3, 0))
    row.paste(im5, (im4.width*4, 0))
    return row


def make_column(row1, row2, row3, row4):
    column = Image.new('RGB', (row1.width, row1.height*4))
    column.paste(row1, (0, 0))
    column.paste(row2, (0, row1.height))
    column.paste(row3, (0, row2.height*2))
    column.paste(row4, (0, row3.height*3))
    return column



import random

#the card class take the suit and the value as attributes and create each individual cards.
#the class models each individual cards
#It used the name list which contain different value of the card in english
class Card:
    name = ("two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king", "ace")

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit

    def get_name(self):
        return Card.name[self.value - 2] + " of " + self.suit

    def image_file_name(self):
        if self.value < 11:
            return str(self.value) + "_of_" + self.suit + ".png"
        else:
            return Card.name[self.value - 2] + "_of_" + self.suit + ".png"

#the deck class models 52 cards
#it takes a list of cards as a attribute and append cards to it
#after the card is added to the list, the card is shuffle it randomly
#then it deal the card to different hands
class Deck:
    suits = ("spades", "clubs", "hearts", "diamonds")

    def __init__(self):
        self.cards = []
        for s in Deck.suits:
            for i in range(2, 14):
                self.cards.append(Card(s, i))

    def get_deck(self):
        return self.cards

    def print_deck(self):
        print([y.get_name() for y in self.cards])

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) == 0:
            return None
        else:
            top = self.cards[0]
            self.cards.remove(top)
            return top

def get_key(obj):
    return obj.value

#the hand class models each individual hand in the poker game
#it takes the dealt cards as a attribute and creates a list
#the list contains cards from the deck
#the class mostly uses loops to compare cards and to identify what kind of rank it is
#then it compares the number of the rank to determine which one is bigger
#if the number is the same, it goes through a series of algorithm to find the winner
class Hand:
    def __init__(self):
        self.cards_dealt = []

    def get_hand(self):
        return self.cards_dealt

    def print_hand(self):
        print([x.get_name() for x in self.cards_dealt])

    def add_card(self, card):
        self.cards_dealt.append(card)
        self.cards_dealt.sort(key=get_key)

    def rank(self):
        if self.royal_flush():
            return 9
        if self.straight_flush():
            return 8
        if self.four_of_a_kind():
            return 7
        if self.full_house():
            return 6
        if self.flush():
            return 5
        if self.straight():
            return 4
        if self.three_of_a_kind():
            return 3
        if self.two_pair():
            return 2
        if self.one_pair():
            return 1
        else:
            return 0

    def get_hand_type(self):
        if self.rank() == 9:
            return 'royal_flush'
        if self.rank() == 9:
            return 'straight flush'
        if self.rank() == 7:
            return 'four of a kind'
        if self.rank() == 6:
            return 'full house'
        if self.rank() == 5:
            return 'flush'
        if self.rank() == 4:
            return 'straight'
        if self.rank() == 3:
            return 'three of a kind'
        if self.rank() == 2:
            return 'two pair'
        if self.rank() == 1:
            return 'one pair'
        else:
            return 'high card'

    def royal_flush(self):
        if self.cards_dealt[0].value == 10 and all(card.value >= 10 for card in self.cards_dealt):
            return self.flush()
        return False

    def straight_flush(self):
        if self.straight() and self.flush():
            return True
        return False

    def four_of_a_kind(self):
        if self.cards_dealt[0].value == self.cards_dealt[3].value or self.cards_dealt[1].value == self.cards_dealt[
            4].value:
            return True
        return False

    def full_house(self):
        if (self.cards_dealt[0].value == self.cards_dealt[1].value == self.cards_dealt[2].value and
                self.cards_dealt[3].value == self.cards_dealt[4].value):
            return True
        elif (self.cards_dealt[0].value == self.cards_dealt[1].value and
              self.cards_dealt[2].value == self.cards_dealt[3].value == self.cards_dealt[4].value):
            return True
        return False

    def flush(self):
        return all(card.suit == self.cards_dealt[0].suit for card in self.cards_dealt)

    def straight(self):
        values = [card.value for card in self.cards_dealt]
        values.sort()
        return values == list(range(values[0], values[0] + 5))

    def three_of_a_kind(self):
        if (self.cards_dealt[0].value == self.cards_dealt[1].value == self.cards_dealt[2].value or
                self.cards_dealt[2].value == self.cards_dealt[3].value == self.cards_dealt[4].value):
            return True
        return False

    def two_pair(self):
        pairs = 0
        for i in range(4):
            if self.cards_dealt[i].value == self.cards_dealt[i + 1].value:
                pairs += 1
        return pairs == 2

    def one_pair(self):
        for i in range(4):
            if self.cards_dealt[i].value == self.cards_dealt[i + 1].value:
                return True
        return False

    def high_card(self, hand):
        for i in range(4, -1, -1):
            if self.cards_dealt[i].value > hand.cards_dealt[i].value:
                return 1
            elif self.cards_dealt[i].value < hand.cards_dealt[i].value:
                return -1
        return 0

    def compare(self, hand):
        if self.rank() > hand.rank():
            return 1
        elif self.rank() < hand.rank():
            return -1
        elif self.rank() == hand.rank() and self.rank() == 9:
            return 0
        elif self.rank() == hand.rank() and (self.rank() == 8 or self.rank() == 5 or self.rank() == 4):
            return self.high_card(hand)
        elif self.rank() == hand.rank() and (self.rank() == 7 or self.rank() == 6 or self.rank() == 3):
            if self.cards_dealt[3].value > hand.cards_dealt[3].value:
                return 1
            elif self.cards_dealt[3].value < hand.cards_dealt[3].value:
                return -1
            else:
                return 0
        elif self.rank() == hand.rank() and self.rank() == 2:
            for i in range(0, 4):
                if self.cards_dealt[i].value == self.cards_dealt[i + 1].value:
                    self_pair_value = self.cards_dealt[i].value
                    break
            for j in range(i + 2, 4):
                if self.cards_dealt[j].value == self.cards_dealt[j + 1].value:
                    self_pair_value = self.cards_dealt[j].value
                    break
            for a in range(0, 4):
                if hand.cards_dealt[a].value == hand.cards_dealt[a + 1].value:
                    hand_pair_value = hand.cards_dealt[a].value
                    break
            for b in range(a + 2, 4):
                if hand.cards_dealt[b].value == hand.cards_dealt[b + 1].value:
                    hand_pair_value = hand.cards_dealt[b].value
                    break

            if self_pair_value > hand_pair_value:
                return 1
            elif self_pair_value < hand_pair_value:
                return -1
            else:
                return 0

        elif self.rank() == hand.rank() and self.rank() == 1:
            for i in range(0, 4):
                if self.cards_dealt[i].value == self.cards_dealt[i + 1].value:
                    return self.cards_dealt[i].value
            for a in range(0, 4):
                if hand.cards_dealt[a].value == hand.cards_dealt[a + 1].value:
                    return hand.cards_dealt[a].value
            if a < i:
                return 1
            elif a > i:
                return -1


def winner(hands):
    win = hands[0]
    for hand in hands[1:]:
        comparison = hand.compare(win)
        if comparison == 1:
            win = hand
        elif comparison == -1:
            continue
        elif comparison == 0:
            win = None
    return win


if __name__ == "__main__":
    a = Deck()
    a.shuffle()
    a.print_deck()

    poker_game = [Hand() for i in range(4)]

    for hand in poker_game:
        for i in range(0, 5):
            hand.add_card(a.deal_card())
        hand.print_hand()

    x = make_row(Image.open("cards/" + poker_game[0].cards_dealt[0].image_file_name()),
                 Image.open("cards/" + poker_game[0].cards_dealt[1].image_file_name()),
                 Image.open("cards/" + poker_game[0].cards_dealt[2].image_file_name()),
                 Image.open("cards/" + poker_game[0].cards_dealt[3].image_file_name()),
                 Image.open("cards/" + poker_game[0].cards_dealt[4].image_file_name()))

    y = make_row(Image.open("cards/" + poker_game[1].cards_dealt[0].image_file_name()),
                 Image.open("cards/" + poker_game[1].cards_dealt[1].image_file_name()),
                 Image.open("cards/" + poker_game[1].cards_dealt[2].image_file_name()),
                 Image.open("cards/" + poker_game[1].cards_dealt[3].image_file_name()),
                 Image.open("cards/" + poker_game[1].cards_dealt[4].image_file_name()))

    z = make_row(Image.open("cards/" + poker_game[2].cards_dealt[0].image_file_name()),
                 Image.open("cards/" + poker_game[2].cards_dealt[1].image_file_name()),
                 Image.open("cards/" + poker_game[2].cards_dealt[2].image_file_name()),
                 Image.open("cards/" + poker_game[2].cards_dealt[3].image_file_name()),
                 Image.open("cards/" + poker_game[2].cards_dealt[4].image_file_name()))

    w = make_row(Image.open("cards/" + poker_game[3].cards_dealt[0].image_file_name()),
                 Image.open("cards/" + poker_game[3].cards_dealt[1].image_file_name()),
                 Image.open("cards/" + poker_game[3].cards_dealt[2].image_file_name()),
                 Image.open("cards/" + poker_game[3].cards_dealt[3].image_file_name()),
                 Image.open("cards/" + poker_game[3].cards_dealt[4].image_file_name()))

    o = make_column(x, y, z, w)
    draw = ImageDraw.Draw(o)

    myFont = ImageFont.truetype('Arial', 15)
    WinnerFont = ImageFont.truetype('Arial', 25)

    text = poker_game[0].get_hand_type()
    draw.text((510, 100), text, font=myFont, fill=(255, 255, 255))

    text = poker_game[1].get_hand_type()
    draw.text((510, 250), text, font=myFont, fill=(255, 255, 255))

    text = poker_game[2].get_hand_type()
    draw.text((510, 400), text, font=myFont, fill=(255, 255, 255))

    text = poker_game[3].get_hand_type()
    draw.text((510, 550), text, font=myFont, fill=(255, 255, 255))

    if winner(poker_game) == poker_game[0]:
        draw.text((510, 50), 'Winner', font=WinnerFont, fill=(255, 0, 0))
    elif winner(poker_game) == poker_game[1]:
        draw.text((510, 200), 'Winner', font=WinnerFont, fill=(255, 0, 0))
    elif winner(poker_game) == poker_game[2]:
        draw.text((510, 350), 'Winner', font=WinnerFont, fill=(255, 0, 0))
    elif winner(poker_game) == poker_game[3]:
        draw.text((510, 500), 'Winner', font=WinnerFont, fill=(255, 0, 0))

    o.show()






