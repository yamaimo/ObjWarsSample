import random
from typing import Any, Callable, NewType, Optional

from action import (
    Action,
    ActionList,
    ActionList_contains_action,
    ActionList_get_all_actions,
    ActionList_get_ask_actions,
    ActionList_get_guess_actions,
    AskAction_get_card,
    AskAction_init,
    GuessAction_get_card,
    GuessAction_init,
)
from card import (
    Card,
    Card_init,
    Card_to_str,
    Hand,
    Hand_get_cards,
)
from terminal import (
    Terminal,
    Terminal_get_str,
    Terminal_put_empty_line,
    Terminal_put_str,
)

# HumanPlayer ====================

HumanPlayer = NewType("HumanPlayer", tuple[str, Hand, Terminal])


def HumanPlayer_init(
    name: str, hand: Hand, terminal: Terminal
) -> HumanPlayer:
    data = (name, hand, terminal)
    return HumanPlayer(data)


def HumanPlayer_get_name(player: HumanPlayer) -> str:
    return player[0]


def HumanPlayer_select_action(
    player: HumanPlayer, available_actions: ActionList
) -> Action:
    name = player[0]

    hand = player[1]
    hand_str = ", ".join(map(Card_to_str, Hand_get_cards(hand)))

    terminal = player[2]

    ask_actions = ActionList_get_ask_actions(available_actions)
    ask_cards = map(AskAction_get_card, ask_actions)
    ask_cards_str = ", ".join(map(Card_to_str, ask_cards))

    guess_actions = ActionList_get_guess_actions(
        available_actions
    )
    guess_cards = map(GuessAction_get_card, guess_actions)
    guess_cards_str = ", ".join(map(Card_to_str, guess_cards))

    while True:
        Terminal_put_str(terminal, f"{name} hand: {hand_str}")
        Terminal_put_str(terminal, "Available commands:")
        if ask_cards_str:
            Terminal_put_str(
                terminal,
                f"  ask <card>      (<card>: {ask_cards_str})",
            )
        if guess_cards_str:
            Terminal_put_str(
                terminal,
                f"  guess <card>    (<card>: {guess_cards_str})",
            )
        Terminal_put_str(terminal, "  exit")

        input_str = Terminal_get_str(terminal, f"{name}> ")
        args = input_str.strip().split()
        if len(args) < 1:
            Terminal_put_str(terminal, "Empty Command.")
            Terminal_put_empty_line(terminal)
            continue

        command = args[0].lower()
        card: Optional[Card] = None
        if len(args) >= 2:
            try:
                card = Card_init(int(args[1]))
            except Exception as e:
                Terminal_put_str(terminal, str(e))
                Terminal_put_empty_line(terminal)
                continue

        if command == "ask":
            if card is None:
                Terminal_put_str(
                    terminal, "Card is not specified."
                )
                Terminal_put_empty_line(terminal)
                continue
            action = AskAction_init(card)
        elif command == "guess":
            if card is None:
                Terminal_put_str(
                    terminal, "Card is not specified."
                )
                Terminal_put_empty_line(terminal)
                continue
            action = GuessAction_init(card)
        elif command == "exit":
            raise Exception("Exit game.")
        else:
            Terminal_put_str(
                terminal,
                f"Unknown Command. (command: {command})",
            )
            Terminal_put_empty_line(terminal)
            continue

        if not ActionList_contains_action(
            available_actions, action
        ):
            Terminal_put_str(
                terminal, f"Unavailable. (action: {action})"
            )
            Terminal_put_empty_line(terminal)
            continue
        else:
            return action


# RandomAI ====================

RandomAI = NewType("RandomAI", tuple[str])


def RandomAI_init(
    name: str, random_state: Optional[int] = None
) -> RandomAI:
    random.seed(random_state)
    data = (name,)
    return RandomAI(data)


def RandomAI_get_name(player: RandomAI) -> str:
    return player[0]


def RandomAI_select_action(
    player: RandomAI, available_actions: ActionList
) -> Action:
    return random.choice(
        ActionList_get_all_actions(available_actions)
    )


# Player ====================

NameFunc = Callable[[Any], str]
SelectActionFunc = Callable[[Any, ActionList], Action]

Player = NewType(
    "Player", tuple[Any, NameFunc, SelectActionFunc]
)


def Player_init_with_human_player(
    human_player: HumanPlayer,
) -> Player:
    data = (
        human_player,
        HumanPlayer_get_name,
        HumanPlayer_select_action,
    )
    return Player(data)


def Player_init_with_random_ai(random_ai: RandomAI) -> Player:
    data = (
        random_ai,
        RandomAI_get_name,
        RandomAI_select_action,
    )
    return Player(data)


def Player_get_name(player: Player) -> str:
    player_impl = player[0]
    name_func = player[1]
    return name_func(player_impl)


def Player_select_action(
    player: Player, available_actions: ActionList
) -> Action:
    player_impl = player[0]
    select_action_func = player[2]
    return select_action_func(player_impl, available_actions)


if __name__ == "__main__":
    from io import StringIO

    from action import ActionList_get_available_actions
    from card import (
        Deal_get_player0_hand,
        Dealer_deal,
        Dealer_init,
    )
    from terminal import Terminal_init

    dealer = Dealer_init(0)
    deal = Dealer_deal(dealer)
    hand = Deal_get_player0_hand(deal)

    terminal = Terminal_init(
        in_stream=StringIO("ask 1\nguess 2\n")
    )

    # HumanPlayer
    human = HumanPlayer_init("human", hand, terminal)
    player = Player_init_with_human_player(human)
    name = Player_get_name(player)

    available_actions = ActionList_get_available_actions(
        hand, None
    )
    action = Player_select_action(player, available_actions)
    print(f"{name} select {action}")
    print()

    available_actions = ActionList_get_available_actions(
        hand, action
    )
    action = Player_select_action(player, available_actions)
    print(f"{name} select {action}")
    print()

    # RandomAI
    rand_ai = RandomAI_init("random", 0)
    player = Player_init_with_random_ai(rand_ai)
    name = Player_get_name(player)

    available_actions = ActionList_get_available_actions(
        hand, None
    )
    action = Player_select_action(player, available_actions)
    print(f"{name} select {action}")
    print()

    available_actions = ActionList_get_available_actions(
        hand, action
    )
    action = Player_select_action(player, available_actions)
    print(f"{name} select {action}")
    print()
