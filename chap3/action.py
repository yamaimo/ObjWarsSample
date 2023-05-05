from typing import NewType, Optional, Union

from card import Card, Card_get_all_cards, Hand, Hand_has_card

# AskAction ====================

AskAction = NewType("AskAction", tuple[str, Card])

ACTION_KIND_ASK = "ask"


def AskAction_init(card: Card) -> AskAction:
    """質問を生成して返す"""
    data = (ACTION_KIND_ASK, card)
    return AskAction(data)


def AskAction_get_card(action: AskAction) -> Card:
    """質問したカードを返す"""
    return action[1]


def AskAction_is_hit(action: AskAction, hand: Hand) -> bool:
    """質問したカードが手札にあるか返す"""
    return Hand_has_card(hand, action[1])  # type: ignore


# GuessAction ====================

GuessAction = NewType("GuessAction", tuple[str, Card])

ACTION_KIND_GUESS = "guess"


def GuessAction_init(card: Card) -> GuessAction:
    """推測を生成して返す"""
    data = (ACTION_KIND_GUESS, card)
    return GuessAction(data)


def GuessAction_get_card(action: GuessAction) -> Card:
    """推測したカードを返す"""
    return action[1]


def GuessAction_is_hit(action: GuessAction, rest_card: Card) -> bool:
    """推測したカードが残りのカードと一致するか返す"""
    return action[1] == rest_card  # type: ignore


# Action ====================

Action = Union[AskAction, GuessAction]


def Action_is_ask(action: Action) -> bool:
    """行動が質問かを返す"""
    return action[0] == ACTION_KIND_ASK


def Action_is_guess(action: Action) -> bool:
    """行動が推測かを返す"""
    return action[0] == ACTION_KIND_GUESS


# ActionList ====================

ActionList = NewType("ActionList", tuple[list[AskAction], list[GuessAction]])


def ActionList_init(
    ask_actions: list[AskAction], guess_actions: list[GuessAction]
) -> ActionList:
    """行動の一覧を生成して返す"""
    data = (ask_actions, guess_actions)
    return ActionList(data)


def ActionList_get_ask_actions(action_list: ActionList) -> list[AskAction]:
    """質問の一覧を返す"""
    return action_list[0]


def ActionList_get_guess_actions(action_list: ActionList) -> list[GuessAction]:
    """推測の一覧を返す"""
    return action_list[1]


def ActionList_get_all_actions(action_list: ActionList) -> list[Action]:
    """行動の一覧を返す"""
    return action_list[0] + action_list[1]  # type: ignore


def ActionList_contains_action(action_list: ActionList, action: Action) -> bool:
    """指定された行動が一覧に含まれるか返す"""
    return action in ActionList_get_all_actions(action_list)


def ActionList_get_available_actions(
    hand: Hand, prev_action: Optional[AskAction]
) -> ActionList:
    """
    手番プレイヤーの手札と直前の行動から
    選択可能な行動の一覧を生成して返す
    """
    ask_actions = [AskAction_init(card) for card in Card_get_all_cards()]
    guess_actions = []

    if prev_action is not None:
        ask_actions.remove(prev_action)
        for card in Card_get_all_cards():
            if not Hand_has_card(hand, card):
                guess_actions.append(GuessAction_init(card))

    return ActionList_init(ask_actions, guess_actions)


if __name__ == "__main__":
    from card import (
        Card_init,
        Deal_get_player0_hand,
        Deal_get_player1_hand,
        Deal_get_rest_card,
        Dealer_deal,
        Dealer_init,
    )

    dealer = Dealer_init(0)
    deal = Dealer_deal(dealer)

    ask = AskAction_init(Card_init(1))
    print(ask)
    print(AskAction_is_hit(ask, Deal_get_player1_hand(deal)))

    guess = GuessAction_init(Card_init(2))
    print(guess)
    print(GuessAction_is_hit(guess, Deal_get_rest_card(deal)))

    print(ActionList_get_available_actions(Deal_get_player0_hand(deal), None))
    print(
        ActionList_get_available_actions(
            Deal_get_player1_hand(deal),
            AskAction_init(Card_init(1)),
        )
    )
    print(
        ActionList_get_available_actions(
            Deal_get_player0_hand(deal),
            AskAction_init(Card_init(2)),
        )
    )
