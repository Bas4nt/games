import random
from telegram import Update
from telegram.ext import CallbackContext

games = {}  # chat_id -> UnoGame

colors = ["Red", "Green", "Blue", "Yellow"]
numbers = list(range(0, 10))

class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def matches(self, other):
        return self.color == other.color or self.number == other.number

    def __str__(self):
        return f"{self.color} {self.number}"

class UnoGame:
    def __init__(self):
        self.players = []
        self.hands = {}
        self.deck = [Card(c, n) for c in colors for n in numbers * 2]
        random.shuffle(self.deck)
        self.current_card = self.deck.pop()
        self.turn = 0
        self.active = False

    def join(self, user):
        if self.active:
            return "Game already started!"
        if user.id in [p.id for p in self.players]:
            return f"{user.first_name} already joined."
        if len(self.players) >= 4:
            return "Max 4 players allowed!"
        self.players.append(user)
        return f"{user.first_name} joined the game!"

    def start(self):
        if len(self.players) < 2:
            return "Need at least 2 players to start!"
        self.active = True
        for player in self.players:
            self.hands[player.id] = [self.deck.pop() for _ in range(7)]
        return f"Game started! Current card: {self.current_card}. {self.players[0].first_name}'s turn."

    def hand(self, user_id):
        return ", ".join(str(card) for card in self.hands[user_id])

    def current_player(self):
        return self.players[self.turn]

    def play_card(self, user, color, number):
        if not self.active:
            return "Game hasn't started yet!"
        if self.players[self.turn].id != user.id:
            return f"Not your turn. It's {self.players[self.turn].first_name}'s turn."

        card = Card(color, int(number))
        hand = self.hands[user.id]

        for c in hand:
            if c.color == card.color and c.number == card.number:
                if not c.matches(self.current_card):
                    return f"{c} does not match current card {self.current_card}"
                self.current_card = c
                hand.remove(c)
                if not hand:
                    self.active = False
                    return f"{user.first_name} wins the game!"
                self.turn = (self.turn + 1) % len(self.players)
                return f"{user.first_name} played {c}. Next: {self.players[self.turn].first_name}."
        return f"You don't have {card} in your hand."

def get_game(chat_id):
    if chat_id not in games:
        games[chat_id] = UnoGame()
    return games[chat_id]

def uno_join(update: Update, context: CallbackContext):
    game = get_game(update.effective_chat.id)
    user = update.effective_user
    result = game.join(user)
    update.message.reply_text(result)

def uno_start(update: Update, context: CallbackContext):
    game = get_game(update.effective_chat.id)
    update.message.reply_text(game.start())

def uno_play(update: Update, context: CallbackContext):
    args = context.args
    if len(args) != 2:
        update.message.reply_text("Usage: /play <color> <number> (e.g. /play red 3)")
        return
    color = args[0].capitalize()
    number = args[1]
    if color not in colors or not number.isdigit():
        update.message.reply_text("Invalid color or number.")
        return
    game = get
