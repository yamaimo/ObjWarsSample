from typing import Optional, Protocol, cast

from action import ActionList, AskAction, GuessAction
from card import Deal
from player import Player
from terminal import Terminal


class GameObserver(Protocol):
    def player_asked(self, player: Player, ask: AskAction, is_hit: bool) -> None:
        """プレイヤーが質問したときに実行される"""
        ...

    def player_guessed(self, player: Player, guess: GuessAction, is_hit: bool) -> None:
        """プレイヤーが推測したときに実行される"""
        ...


class Game:
    def __init__(self, deal: Deal, player0: Player, player1: Player) -> None:
        """ゲームを初期化する"""
        self.__deal = deal
        self.__player0 = player0
        self.__player1 = player1
        self.__observers: set[GameObserver] = set()

    def add_observer(self, observer: GameObserver) -> None:
        """オブザーバを追加する"""
        self.__observers.add(observer)

    def remove_observer(self, observer: GameObserver) -> None:
        """オブザーバを取り除く"""
        self.__observers.remove(observer)

    def start(self) -> Player:
        """ゲームを開始し、勝ったプレイヤーを返す"""
        turn_player = self.__player0
        turn_hand = self.__deal.player0_hand
        opponent_player = self.__player1
        opponent_hand = self.__deal.player1_hand
        rest_card = self.__deal.rest_card

        prev_action: Optional[AskAction] = None
        while True:
            available_actions = ActionList.get_available_actions(turn_hand, prev_action)
            action = turn_player.select_action(available_actions)

            if isinstance(action, AskAction):
                ask = cast(AskAction, action)
                is_hit = ask.is_hit(opponent_hand)
                self.__notify_ask(turn_player, ask, is_hit)
            else:
                guess = cast(GuessAction, action)
                is_hit = guess.is_hit(rest_card)
                self.__notify_guess(turn_player, guess, is_hit)
                win_player = turn_player if is_hit else opponent_player
                return win_player

            prev_action = ask
            turn_player, opponent_player = opponent_player, turn_player
            turn_hand, opponent_hand = opponent_hand, turn_hand

    def __notify_ask(self, player: Player, ask: AskAction, is_hit: bool) -> None:
        for observer in self.__observers:
            observer.player_asked(player, ask, is_hit)

    def __notify_guess(self, player: Player, guess: GuessAction, is_hit: bool) -> None:
        for observer in self.__observers:
            observer.player_guessed(player, guess, is_hit)


class GameView(GameObserver):
    def __init__(self, terminal: Terminal) -> None:
        """表示を初期化する"""
        self.__terminal = terminal

    def player_asked(self, player: Player, ask: AskAction, is_hit: bool) -> None:
        """プレイヤーの質問内容と結果を表示する"""
        self.__terminal.put_str(f"{player.name}: {ask}")
        result = "Hit." if is_hit else "Miss."
        self.__terminal.put_str(result)
        self.__terminal.put_empty_line()

    def player_guessed(self, player: Player, guess: GuessAction, is_hit: bool) -> None:
        """プレイヤーの推測内容と結果を表示する"""
        self.__terminal.put_str(f"{player.name}: {guess}")
        result = "Hit." if is_hit else "Miss."
        self.__terminal.put_str(result)
        self.__terminal.put_empty_line()


if __name__ == "__main__":
    from io import StringIO

    from card import Dealer
    from player import HumanPlayer

    deal = Dealer(0).deal()

    terminal0 = Terminal(in_stream=StringIO("ask 2\nguess 4\n"))
    human0 = HumanPlayer("player0", deal.player0_hand, terminal0)
    terminal1 = Terminal(in_stream=StringIO("ask 3\n"))
    human1 = HumanPlayer("player1", deal.player1_hand, terminal1)

    terminal = Terminal()
    game = Game(deal, human0, human1)
    view = GameView(terminal)
    game.add_observer(view)
    win_player = game.start()
    print(f"{win_player.name} won.")
