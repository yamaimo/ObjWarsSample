from typing import Any, Optional, Union

from card import Card, Hand


class AskAction:
    def __init__(self, card: Card) -> None:
        """質問を初期化する"""
        self.__card = card

    @property
    def card(self) -> Card:
        """質問したカードを返す"""
        return self.__card

    def is_hit(self, hand: Hand) -> bool:
        """質問したカードが手札にあるか返す"""
        return hand.has_card(self.__card)  # type: ignore

    def __repr__(self) -> str:
        """質問を表現する文字列を返す"""
        return f"Ask({self.__card})"

    def __eq__(self, other: Any) -> bool:
        """質問が同じか返す"""
        return isinstance(other, AskAction) and (self.__card == other.card)


class GuessAction:
    def __init__(self, card: Card) -> None:
        """推測を初期化する"""
        self.__card = card

    @property
    def card(self) -> Card:
        """推測したカードを返す"""
        return self.__card

    def is_hit(self, rest_card: Card) -> bool:
        """推測したカードが残りのカードと一致するか返す"""
        return self.__card == rest_card  # type: ignore

    def __repr__(self) -> str:
        """推測を表現する文字列を返す"""
        return f"Guess({self.__card})"

    def __eq__(self, other: Any) -> bool:
        """推測が同じか返す"""
        return isinstance(other, GuessAction) and (self.__card == other.card)


Action = Union[AskAction, GuessAction]


class ActionList:
    def __init__(
        self, ask_actions: list[AskAction], guess_actions: list[GuessAction]
    ) -> None:
        """行動の一覧を初期化する"""
        self.__ask_actions = ask_actions
        self.__guess_actions = guess_actions

    @property
    def ask_actions(self) -> list[AskAction]:
        """質問の一覧を返す"""
        return self.__ask_actions

    @property
    def guess_actions(self) -> list[GuessAction]:
        """推測の一覧を返す"""
        return self.__guess_actions

    @property
    def all_actions(self) -> list[Action]:
        """行動の一覧を返す"""
        return self.__ask_actions + self.__guess_actions  # type: ignore

    def __contains__(self, action: Action) -> bool:
        """指定された行動が一覧に含まれるか返す"""
        return action in self.all_actions

    def __repr__(self) -> str:
        """行動の一覧を表現する文字列を返す"""
        return self.all_actions.__repr__()

    @classmethod
    def get_available_actions(
        cls, hand: Hand, prev_action: Optional[AskAction]
    ) -> "ActionList":
        """
        手番プレイヤーの手札と直前の行動から
        選択可能な行動の一覧を生成して返す
        """
        ask_actions = [AskAction(card) for card in Card.get_all_cards()]
        guess_actions = []

        if prev_action is not None:
            ask_actions.remove(prev_action)
            for card in Card.get_all_cards():
                if not hand.has_card(card):
                    guess_actions.append(GuessAction(card))

        return cls(ask_actions, guess_actions)


if __name__ == "__main__":
    from card import Card, Dealer

    deal = Dealer(0).deal()

    ask = AskAction(Card(1))
    print(ask)
    print(ask.is_hit(deal.player0_hand))

    guess = GuessAction(Card(2))
    print(guess)
    print(guess.is_hit(deal.rest_card))

    print(ActionList.get_available_actions(deal.player0_hand, None))
    print(
        ActionList.get_available_actions(
            deal.player1_hand,
            AskAction(Card(1)),
        )
    )
    print(
        ActionList.get_available_actions(
            deal.player0_hand,
            AskAction(Card(2)),
        )
    )
