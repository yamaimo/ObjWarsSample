from card import Dealer, Hand
from game import Game
from player import Player, RandomAI
from smartai import SmartAI
from terminal import Terminal


def create_player(
    player_type: str, name: str, hand: Hand
) -> Player:
    """プレイヤーを作って返す"""
    if player_type == "random":
        return RandomAI(name)
    elif player_type == "smart":
        return SmartAI(name, hand)
    else:
        raise ValueError(
            f"Unknown player type. (type: {player_type})"
        )


def main(
    repeat_count: int, player0_type: str, player1_type: str
) -> None:
    """メイン"""
    assert (
        repeat_count > 0
    ), f"Invalid repeat count. (count: {repeat_count})"
    player0_win_count = 0
    player1_win_count = 0
    terminal = Terminal()
    for i in range(repeat_count):
        deal = Dealer().deal()

        player0 = create_player(
            player0_type, "Player0", deal.player0_hand
        )
        player1 = create_player(
            player1_type, "Player1", deal.player1_hand
        )

        game = Game(deal, player0, player1)

        if isinstance(player0, SmartAI):
            game.add_observer(player0)
        if isinstance(player1, SmartAI):
            game.add_observer(player1)

        win_player = game.start()
        terminal.put_str(
            f"[{i}/{repeat_count}] {win_player.name} won."
        )
        if win_player == player0:
            player0_win_count += 1
        else:
            player1_win_count += 1
    player0_win_rate = player0_win_count * 100 / repeat_count
    player1_win_rate = player1_win_count * 100 / repeat_count
    terminal.put_str(
        f"Player0 ({player0_type}): {player0_win_rate:6.2f}%"
    )
    terminal.put_str(
        f"Player1 ({player1_type}): {player1_win_rate:6.2f}%"
    )


if __name__ == "__main__":
    import argparse

    player_types = ["random", "smart"]

    parser = argparse.ArgumentParser()
    parser.add_argument("repeat_count", type=int)
    parser.add_argument("player0_type", choices=player_types)
    parser.add_argument("player1_type", choices=player_types)

    args = parser.parse_args()
    repeat_count = args.repeat_count
    player0_type = args.player0_type
    player1_type = args.player1_type

    main(repeat_count, player0_type, player1_type)
