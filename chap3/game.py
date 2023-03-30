from typing import NewType, Optional, cast

from action import (
    Action_is_ask,
    ActionList_get_available_actions,
    AskAction,
    AskAction_get_card,
    AskAction_is_hit,
    GuessAction,
    GuessAction_get_card,
    GuessAction_is_hit,
)
from card import (
    Card_to_str,
    Deal,
    Deal_get_player0_hand,
    Deal_get_player1_hand,
    Deal_get_rest_card,
)
from player import Player, Player_get_name, Player_select_action
from terminal import (
    Terminal,
    Terminal_put_empty_line,
    Terminal_put_str,
)

# Game ====================

Game = NewType("Game", tuple[Deal, Player, Player, Terminal])


def Game_init(
    deal: Deal,
    player0: Player,
    player1: Player,
    terminal: Terminal,
) -> Game:
    data = (deal, player0, player1, terminal)
    return Game(data)


def Game_start(game: Game) -> Player:
    deal = game[0]
    turn_player = game[1]
    opponent_player = game[2]
    terminal = game[3]

    turn_hand = Deal_get_player0_hand(deal)
    opponent_hand = Deal_get_player1_hand(deal)
    rest_card = Deal_get_rest_card(deal)

    prev_action: Optional[AskAction] = None
    while True:
        turn_player_name = Player_get_name(turn_player)
        available_actions = ActionList_get_available_actions(
            turn_hand, prev_action
        )
        action = Player_select_action(
            turn_player, available_actions
        )

        if Action_is_ask(action):
            ask_action = cast(AskAction, action)
            card_str = Card_to_str(
                AskAction_get_card(ask_action)
            )
            Terminal_put_str(
                terminal, f"{turn_player_name} asked {card_str}"
            )

            is_hit = AskAction_is_hit(ask_action, opponent_hand)
            result = "Hit." if is_hit else "Miss."
            Terminal_put_str(terminal, result)
            Terminal_put_empty_line(terminal)
        else:
            guess_action = cast(GuessAction, action)
            card_str = Card_to_str(
                GuessAction_get_card(guess_action)
            )
            Terminal_put_str(
                terminal,
                f"{turn_player_name} guessed {card_str}",
            )

            is_hit = GuessAction_is_hit(guess_action, rest_card)
            result = "Hit." if is_hit else "Miss."
            Terminal_put_str(terminal, result)
            Terminal_put_empty_line(terminal)

            win_player = (
                turn_player if is_hit else opponent_player
            )
            return win_player

        prev_action = ask_action
        turn_player, opponent_player = (
            opponent_player,
            turn_player,
        )
        turn_hand, opponent_hand = opponent_hand, turn_hand


if __name__ == "__main__":
    from io import StringIO

    from card import Dealer_deal, Dealer_init
    from player import (
        HumanPlayer_init,
        Player_init_with_human_player,
    )
    from terminal import Terminal_init

    dealer = Dealer_init(0)
    deal = Dealer_deal(dealer)

    terminal = Terminal_init(
        in_stream=StringIO("ask 2\nask 3\nguess 4\n")
    )
    human0 = HumanPlayer_init(
        "player0", Deal_get_player0_hand(deal), terminal
    )
    human1 = HumanPlayer_init(
        "player1", Deal_get_player1_hand(deal), terminal
    )

    player0 = Player_init_with_human_player(human0)
    player1 = Player_init_with_human_player(human1)

    game = Game_init(deal, player0, player1, terminal)
    Game_start(game)
