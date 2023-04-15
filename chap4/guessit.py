from card import Dealer
from game import Game
from player import HumanPlayer, RandomAI
from terminal import Terminal


def main() -> None:
    """メイン"""
    deal = Dealer().deal()

    terminal = Terminal()
    player0 = HumanPlayer(
        "Player0", deal.player0_hand, terminal
    )
    player1 = RandomAI("Player1")

    game = Game(deal, player0, player1, terminal)
    win_player = game.start()

    terminal.put_str(f"{win_player.name} won.")


if __name__ == "__main__":
    main()
