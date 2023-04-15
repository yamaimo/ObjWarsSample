from typing import Optional, cast

from action import ActionList, AskAction, GuessAction
from card import Deal
from player import Player
from terminal import Terminal


class Game:
    def __init__(
        self,
        deal: Deal,
        player0: Player,
        player1: Player,
        terminal: Terminal,
    ) -> None:
        """ゲームを初期化する"""
        self.__deal = deal
        self.__player0 = player0
        self.__player1 = player1
        self.__terminal = terminal

    def start(self) -> Player:
        """ゲームを開始し、勝ったプレイヤーを返す"""
        turn_player = self.__player0
        turn_hand = self.__deal.player0_hand
        opponent_player = self.__player1
        opponent_hand = self.__deal.player1_hand
        rest_card = self.__deal.rest_card

        prev_action: Optional[AskAction] = None
        while True:
            available_actions = (
                ActionList.get_available_actions(
                    turn_hand, prev_action
                )
            )
            action = turn_player.select_action(
                available_actions
            )
            self.__terminal.put_str(
                f"{turn_player.name}: {action}"
            )

            is_hit: bool
            win_player: Optional[Player] = None
            if isinstance(action, AskAction):
                ask_action = cast(AskAction, action)
                is_hit = ask_action.is_hit(opponent_hand)
            else:
                guess_action = cast(GuessAction, action)
                is_hit = guess_action.is_hit(rest_card)
                win_player = (
                    turn_player if is_hit else opponent_player
                )

            result = "Hit." if is_hit else "Miss."
            self.__terminal.put_str(result)
            self.__terminal.put_empty_line()

            if win_player is not None:
                return win_player

            prev_action = ask_action
            turn_player, opponent_player = (
                opponent_player,
                turn_player,
            )
            turn_hand, opponent_hand = opponent_hand, turn_hand


if __name__ == "__main__":
    from io import StringIO

    from card import Dealer
    from player import HumanPlayer

    deal = Dealer(0).deal()

    terminal0 = Terminal(in_stream=StringIO("ask 2\nguess 4\n"))
    human0 = HumanPlayer(
        "player0", deal.player0_hand, terminal0
    )
    terminal1 = Terminal(in_stream=StringIO("ask 3\n"))
    human1 = HumanPlayer(
        "player1", deal.player1_hand, terminal1
    )

    terminal = Terminal()
    game = Game(deal, human0, human1, terminal)
    win_player = game.start()
    print(f"{win_player.name} won.")
