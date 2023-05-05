from card import Deal_get_player0_hand, Dealer_deal, Dealer_init
from game import Game_init, Game_start
from player import (
    HumanPlayer_init,
    Player_get_name,
    Player_init_with_human_player,
    Player_init_with_random_ai,
    RandomAI_init,
)
from terminal import Terminal_init, Terminal_put_str


def main() -> None:
    """メイン"""
    dealer = Dealer_init()
    deal = Dealer_deal(dealer)

    terminal = Terminal_init()
    human = HumanPlayer_init("Player0", Deal_get_player0_hand(deal), terminal)
    ai = RandomAI_init("Player1")

    player0 = Player_init_with_human_player(human)
    player1 = Player_init_with_random_ai(ai)

    game = Game_init(deal, player0, player1, terminal)
    win_player = Game_start(game)

    win_player_name = Player_get_name(win_player)
    Terminal_put_str(terminal, f"{win_player_name} won.")


if __name__ == "__main__":
    main()
