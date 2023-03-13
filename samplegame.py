# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# オブジェクト指向本のサンプルとしてguess itの簡略版を題材とする。

# %% [markdown]
# 1. 1~9のカードを4枚ずつプレイヤーに手札として配り、残り一枚を伏せる
# 2. 各プレイヤーは交互に次のいずれかをおこなう
#     - 相手への質問
#     - 伏せカードの推測
# 3. 相手への質問する場合、ある数字が相手の手札にあるか質問 → 相手はあるかないかを正直に答える
# 4. 伏せカードを推測する場合、当たれば勝ち、外せば負け
# 5. 先手のプレイヤーは最初は質問のみ
# 6. 同じ質問を繰り返すことはできない

# %%
from abc import ABC, abstractmethod
import random
import sys
from typing import Optional, Union, Any


# %%
class Card:
    MIN_VALUE = 1
    MAX_VALUE = 9

    @classmethod
    @property
    def all_cards(cls) -> list["Card"]:
        return [cls(value) for value in range(cls.MIN_VALUE, cls.MAX_VALUE+1)]

    def __init__(self, value: int):
        assert self.MIN_VALUE <= value <= self.MAX_VALUE, f"Invalid value. (value: {value})"
        self.__value = value

    @property
    def value(self) -> int:
        return self.__value

    def __repr__(self) -> str:
        return f"Card({self.__value})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Card) and (self.__value == other.value)

    def __lt__(self, other: "Card") -> bool:
        return self.value < other.value


# %%
class Hand:
    def __init__(self, cards: list[Card]):
        self.__cards = sorted(cards)

    @property
    def cards(self) -> list[Card]:
        return list(self.__cards)

    def has_card(self, card: Card):
        return card in self.__cards


# %%
hand = Hand([Card(1), Card(2), Card(3), Card(4)])
print(hand.cards)
print(hand.has_card(Card(1)))
print(hand.has_card(Card(5)))


# %%
class Deal:
    def __init__(self, player1_hand: Hand, player2_hand: Hand, rest_card: Card):
        # FIXME: カードのチェックした方がいい
        self.__player1_hand = player1_hand
        self.__player2_hand = player2_hand
        self.__rest_card = rest_card

    @property
    def player1_hand(self) -> Hand:
        return self.__player1_hand

    @property
    def player2_hand(self) -> Hand:
        return self.__player2_hand

    @property
    def rest_card(self) -> Card:
        return self.__rest_card


# %%
class Dealer:
    def __init__(self, random_state: Optional[int] = None):
        self.__random_state = random_state

    def deal(self) -> Deal:
        random.seed(self.__random_state)
        all_cards = Card.all_cards
        shuffled_cards = random.sample(all_cards, len(all_cards))
        player1_hand = Hand(shuffled_cards[:4])
        player2_hand = Hand(shuffled_cards[4:8])
        rest_card = shuffled_cards[-1]
        return Deal(player1_hand, player2_hand, rest_card)


# %%
dealer = Dealer()
deal = dealer.deal()
print(deal.player1_hand.cards)
print(deal.player2_hand.cards)
print(deal.rest_card)
deal = dealer.deal()
print(deal.player1_hand.cards)
print(deal.player2_hand.cards)
print(deal.rest_card)


# %%
class AskAction:
    def __init__(self, card: Card):
        self.__card = card

    @property
    def card(self) -> Card:
        return self.__card

    def is_hit(self, hand: Hand) -> bool:
        return hand.has_card(self.__card)

    def __repr__(self) -> str:
        return f"Ask({self.__card})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, AskAction) and (self.__card == other.card)


# %%
class GuessAction:
    def __init__(self, card: Card):
        self.__card = card

    @property
    def card(self) -> Card:
        return self.__card

    def is_hit(self, rest_card: Card) -> bool:
        return self.__card == rest_card

    def __repr__(self) -> str:
        return f"Guess({self.__card})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, GuessAction) and (self.__card == other.card)


# %%
Action = Union[AskAction, GuessAction]

# %%
deal = Dealer(0).deal()

ask = AskAction(Card(1))
print(ask)
print(ask.is_hit(deal.player2_hand))

guess = GuessAction(Card(2))
print(guess)
print(guess.is_hit(deal.rest_card))


# %%
class ActionList:
    def __init__(self, ask_actions: list[AskAction], guess_actions: list[GuessAction]):
        self.__ask_actions = ask_actions
        self.__guess_actions = guess_actions

    @property
    def all_actions(self) -> list[Action]:
        return self.__ask_actions + self.__guess_actions

    @property
    def ask_actions(self) -> list[AskAction]:
        return list(self.__ask_actions)

    @property
    def guess_actions(self) -> list[GuessAction]:
        return list(self.__guess_actions)

    def __contains__(self, action: Action) -> bool:
        return action in self.all_actions

    def __repr__(self) -> str:
        return self.all_actions.__repr__()

    @classmethod
    def get_available_actions(cls, hand: Hand, prev_action: Optional[AskAction]) -> "ActionList":
        ask_actions = [AskAction(card) for card in Card.all_cards]
        guess_actions = []
        if prev_action is not None:
            ask_actions.remove(prev_action)
            guess_actions = [GuessAction(card) for card in Card.all_cards if not hand.has_card(card)]

        return ActionList(ask_actions, guess_actions)


# %%
deal = Dealer(0).deal()

print(ActionList.get_available_actions(deal.player1_hand, None))
print(ActionList.get_available_actions(deal.player2_hand, AskAction(Card(1))))
print(ActionList.get_available_actions(deal.player1_hand, AskAction(Card(2))))


# %%
class ExitException(Exception):
    pass

class Player(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def select_action(self, available_actions: ActionList) -> Action:
        pass


# %%
class HumanPlayer(Player):
    def __init__(self, name: str, hand: Hand):
        self.__name = name
        self.__hand = hand

    @property
    def name(self) -> str:
        return self.__name

    def select_action(self, available_actions: ActionList) -> Action:
        self.__print_help(None, available_actions)
        while True:
            args = input(f"{self.__name}> ").strip().split()
            if len(args) < 1:
                self.__print_help("Empty Command.", available_actions)
                continue

            command = args.pop(0).lower()
            if command == "ask":
                action = self.__parse_ask_command(args)
            elif command == "guess":
                action = self.__parse_guess_command(args)
            elif command == "exit":
                raise ExitException()
            else:
                self.__print_help(f"Unknown Command. (command: {command})", available_actions)
                continue

            if action is None:
                self.__print_help("Parse Error.", available_actions)
                continue
            elif action not in available_actions:
                self.__print_help(f"Unavailable. (action: {action})", available_actions)
                continue
            else:
                return action

    def __print_help(self, message: Optional[str], available_actions: ActionList) -> None:
        if message:
            print(message, file=sys.stderr)
        print(f"Your hand: {self.__format_cards(self.__hand.cards)}")
        print("Available commands:")
        ask_cards = [ask.card for ask in available_actions.ask_actions]
        guess_cards = [guess.card for guess in available_actions.guess_actions]
        if ask_cards:
            print(f"  ask <card>      (<card>: {self.__format_cards(ask_cards)})")
        if guess_cards:
            print(f"  guess <card>    (<card>: {self.__format_cards(guess_cards)})")
        print("  exit")

    def __parse_ask_command(self, args: list[str]) -> Optional[Action]:
        try:
            card = Card(int(args[0]))
            return AskAction(card)
        except (IndexError, ValueError, AssertionError) as e:
            print(e, file=sys.stderr)
            return None

    def __parse_guess_command(self, args: list[str]) -> Optional[Action]:
        try:
            card = Card(int(args[0]))
            return GuessAction(card)
        except (IndexError, ValueError, AssertionError) as e:
            print(e, file=sys.stderr)
            return None

    def __format_cards(self, cards: list[Card]) -> str:
        card_value_strs = [str(card.value) for card in cards]
        return ", ".join(card_value_strs)


# %%
# input()を置き換えるための関数オブジェクト
class TestInput:
    def __init__(self, inputs: list[str]):
        self.__inputs = inputs

    def __call__(self, prompt: str = "") -> str:
        ret = self.__inputs.pop(0)
        print(f"{prompt}{ret}")
        return ret


# %%
deal = Dealer(0).deal()
human = HumanPlayer("human", deal.player1_hand)

org_input = input
input = TestInput(["ask 1", "guess 2"])

available_actions = ActionList.get_available_actions(deal.player1_hand, None)
action = human.select_action(available_actions)
print(action)

available_actions = ActionList.get_available_actions(deal.player1_hand, action)
action = human.select_action(available_actions)
print(action)

input = org_input


# %%
class RandomAI(Player):
    def __init__(self, name: str, random_state: Optional[int] = None):
        self.__name = name
        random.seed(random_state)

    @property
    def name(self) -> str:
        return self.__name

    def select_action(self, available_actions: ActionList) -> Action:
        return random.choice(available_actions.all_actions)


# %%
deal = Dealer(0).deal()
rand_ai = RandomAI("random", 0)

available_actions = ActionList.get_available_actions(deal.player1_hand, None)
action = rand_ai.select_action(available_actions)
print(action)

available_actions = ActionList.get_available_actions(deal.player1_hand, action)
action = rand_ai.select_action(available_actions)
print(action)


# %%
class GameObserver(ABC):
    @abstractmethod
    def player_asked(self, player: Player, ask: AskAction, is_hit: bool) -> None:
        pass

    @abstractmethod
    def player_guessed(self, player: Player, guess: GuessAction, is_hit: bool) -> None:
        pass


# %%
class Game:
    def __init__(self, deal: Deal, player1: Player, player2: Player):
        self.__deal = deal
        self.__player1 = player1
        self.__player2 = player2
        self.__observers: set[GameObserver] = set()

    def add_observer(self, observer: GameObserver) -> None:
        self.__observers.add(observer)

    def remove_observer(self, observer: GameObserver) -> None:
        self.__observers.remove(observer)

    def start(self) -> None:
        turn_player = self.__player1
        opponent_player = self.__player2
        turn_player_hand = self.__deal.player1_hand
        opponent_player_hand = self.__deal.player2_hand

        prev_action = None
        while True:
            available_actions = ActionList.get_available_actions(turn_player_hand, prev_action)
            action = turn_player.select_action(available_actions)

            if isinstance(action, AskAction):
                is_hit = action.is_hit(opponent_player_hand)
                for observer in self.__observers:
                    observer.player_asked(turn_player, action, is_hit)
            else:
                is_hit = action.is_hit(self.__deal.rest_card)
                for observer in self.__observers:
                    observer.player_guessed(turn_player, action, is_hit)
                return

            prev_action = action
            turn_player, opponent_player = opponent_player, turn_player
            turn_player_hand, opponent_player_hand = opponent_player_hand, turn_player_hand


# %%
class GameViewer(GameObserver):
    def player_asked(self, player: Player, ask: AskAction, is_hit: bool) -> None:
        result = "Hit." if is_hit else "Miss."
        print(f"{player.name} asked {ask.card.value} => {result}")

    def player_guessed(self, player: Player, guess: GuessAction, is_hit: bool) -> None:
        result = "Hit." if is_hit else "Miss."
        game_result = "Won." if is_hit else "Lost."
        print(f"{player.name} guessed {guess.card.value} => {result}")
        print(f"{player.name} {game_result}")


# %%
deal = Dealer(0).deal()
player1 = HumanPlayer("player1", deal.player1_hand)
player2 = HumanPlayer("player2", deal.player2_hand)

org_input = input
input = TestInput(["ask 2", "ask 3", "guess 4"])

game = Game(deal, player1, player2)
game.add_observer(GameViewer())
game.start()

input = org_input


# %%
class SmartAI(Player, GameObserver):
    def __init__(self, name, hand: Hand, random_state: Optional[int] = None):
        self.__name = name
        self.__hand = hand
        self.__random_state = random_state
        self.__rest_cards: list[Card] = []   # 残ってるカード
        self.__bluff_cards: list[Card] = []  # ブラフに使えるカード
        self.__maybe_card: Optional[Card] = None  # 推測したカード
        self.__init_state()

    def __init_state(self) -> None:
        self.__rest_cards = [card for card in Card.all_cards if not self.__hand.has_card(card)]
        self.__bluff_cards = list(self.__hand.cards)
        self.__maybe_card = None
        random.seed(self.__random_state)

    @property
    def name(self) -> str:
        return self.__name

    def select_action(self, available_actions: ActionList) -> Action:
        # 推測したカードがあるなら推測する
        if self.__maybe_card is not None:
            guess = GuessAction(self.__maybe_card)
            assert guess in available_actions, \
                f"Invalid action. (action: {guess}, available: {available_actions})"
            return guess

        # そうでない場合、推測可能なら確率で推測する
        available_guess_actions = available_actions.guess_actions
        if available_guess_actions:
            guess_th = 1 / len(self.__rest_cards)
            if random.random() <= guess_th:
                selected = random.choice(self.__rest_cards)
                guess = GuessAction(selected)
                assert guess in available_actions, \
                    f"Invalid action. (action: {guess}, available: {available_actions})"
                return guess

        # そうでない場合、可能なら確率でブラフする
        if self.__bluff_cards:
            bluff_th = (5 - len(self.__bluff_cards)) / 20  # 4枚: 5%, 3枚: 10%, 2枚: 15%, 1枚: 20%
            if random.random() <= bluff_th:
                selected = random.choice(self.__bluff_cards)
                ask = AskAction(selected)
                assert ask in available_actions, \
                    f"Invalid action. (action: {ask}, available: {available_actions})"
                return ask

        # そうでない場合、質問する
        selected = random.choice(self.__rest_cards)
        ask = AskAction(selected)
        assert ask in available_actions, \
            f"Invalid action. (action: {ask}, available: {available_actions})"
        return ask

    def player_asked(self, player: Player, ask: AskAction, is_hit: bool) -> None:
        if player == self:
            if ask.card in self.__bluff_cards:
                self.__bluff_cards.remove(ask.card)
            else:
                self.__rest_cards.remove(ask.card)
                if not is_hit:
                    self.__maybe_card = ask.card
        else:
            if ask.card in self.__bluff_cards:
                self.__bluff_cards.remove(ask.card)
            # ヒットしなかった場合、相手のブラフか残ったカード
            # 確率で推測したカードにし、そうでなければ残ったカードから外す（ブラフと見なして）
            if not is_hit:
                # FIXME: ブラフの確率の閾値を考えた方がいい
                if random.random() <= 0.8:
                    self.__maybe_card = ask.card
                else:
                    if ask.card in self.__rest_cards:
                        self.__rest_cards.remove(ask.card)

    def player_guessed(self, player: Player, guess: GuessAction, is_hit: bool) -> None:
        self.__init_state()


# %%
deal = Dealer().deal()
player1 = SmartAI("player1", deal.player1_hand)
player2 = SmartAI("player2", deal.player2_hand)

game = Game(deal, player1, player2)
game.add_observer(GameViewer())
game.add_observer(player1)
game.add_observer(player2)
game.start()

# %%
