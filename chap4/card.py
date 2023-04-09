import random
from typing import Any, Optional


class Card:
    MIN_NUMBER = 1
    MAX_NUMBER = 9

    def __init__(self, number: int) -> None:
        """
        カードを初期化する
        不正な値の場合はAssertionError
        """
        assert (
            self.MIN_NUMBER <= number <= self.MAX_NUMBER
        ), f"Invalid number. (number: {number})"
        self.__number = number

    @property
    def number(self) -> int:
        """カードの数字を返す"""
        return self.__number

    def __repr__(self) -> str:
        """カードを表現する文字列を返す"""
        return f"Card({self.__number})"

    def __hash__(self) -> int:
        """カードのハッシュ値を返す"""
        return hash(self.__number)

    def __eq__(self, other: Any) -> bool:
        """カードが同じか返す"""
        return isinstance(other, Card) and (
            self.__number == other.number
        )

    def __lt__(self, other: "Card") -> bool:
        """カードの大小比較"""
        return self.number < other.number

    @classmethod
    def get_all_cards(cls) -> list["Card"]:
        """すべてのカードを生成して返す"""
        return [
            cls(number)
            for number in range(
                cls.MIN_NUMBER, cls.MAX_NUMBER + 1
            )
        ]


class Hand:
    def __init__(self, cards: list[Card]) -> None:
        """
        手札を初期化する
        カードのリストが不正な場合はAssertionError
        """
        # 手札のチェック
        assert (
            len(cards) == 4
        ), f"The number of cards is invalid. (cards: {cards})"
        assert (
            len(set(cards)) == 4
        ), f"There are the same cards. (cards: {cards})"

        self.__cards = sorted(cards)

    @property
    def cards(self) -> list[Card]:
        """手札のカード一覧を返す"""
        return self.__cards

    def has_card(self, card: Card) -> bool:
        """手札に指定されたカードがあるか返す"""
        return card in self.__cards


class Deal:
    def __init__(
        self,
        player0_hand: Hand,
        player1_hand: Hand,
        rest_card: Card,
    ) -> None:
        """
        ディールを初期化する
        手札や残ったカードが不正な場合はAssertionError
        """
        # 使われてるカードのチェック
        used_card_set = set(
            player0_hand.cards
            + player1_hand.cards
            + [rest_card]
        )
        all_card_set = set(Card.get_all_cards())
        assert (
            used_card_set == all_card_set
        ), f"Card set is invalid. (used cards: {used_card_set})"

        self.__player0_hand = player0_hand
        self.__player1_hand = player1_hand
        self.__rest_card = rest_card

    @property
    def player0_hand(self) -> Hand:
        """先手の手札を返す"""
        return self.__player0_hand

    @property
    def player1_hand(self) -> Hand:
        """後手の手札を返す"""
        return self.__player1_hand

    @property
    def rest_card(self) -> Card:
        """残ったカードを返す"""
        return self.__rest_card


class Dealer:
    def __init__(
        self, random_state: Optional[int] = None
    ) -> None:
        """ディーラーを初期化する"""
        self.__random_state = random_state

    def deal(self) -> Deal:
        """
        ディーラーにランダムにカードを配らせて
        ディールを生成して返す
        """
        random.seed(self.__random_state)
        all_cards = Card.get_all_cards()
        shuffled_cards = random.sample(
            all_cards, len(all_cards)
        )
        player0_hand = Hand(shuffled_cards[:4])
        player1_hand = Hand(shuffled_cards[4:8])
        rest_card = shuffled_cards[-1]
        return Deal(player0_hand, player1_hand, rest_card)


if __name__ == "__main__":
    # Card ----------

    all_cards = Card.get_all_cards()
    for card in all_cards:
        print(f"number: {card.number}")

    card1_1 = Card(1)
    card1_2 = Card(1)
    card2 = Card(2)
    assert card1_1 == card1_2
    assert card1_1 != card2
    assert card1_2 != card2

    try:
        Card(Card.MIN_NUMBER - 1)
    except Exception as e:
        print(e)
    try:
        Card(Card.MAX_NUMBER + 1)
    except Exception as e:
        print(e)

    # Hand ----------

    hand = Hand([Card(number) for number in range(1, 5)])
    print(hand.cards)
    print(hand.has_card(Card(1)))
    print(hand.has_card(Card(5)))

    try:
        Hand([Card(1), Card(2)])
    except AssertionError as e:
        print(e)
    try:
        Hand([Card(number) for number in [1, 2, 3, 1]])
    except AssertionError as e:
        print(e)

    # Deal ----------

    player0_hand = Hand([Card(i) for i in [1, 5, 7, 8]])
    player1_hand = Hand([Card(i) for i in [2, 4, 6, 9]])
    rest_card = Card(3)
    deal = Deal(player0_hand, player1_hand, rest_card)
    print(deal.player0_hand.cards)
    print(deal.player1_hand.cards)
    print(deal.rest_card)

    try:
        player0_hand = Hand([Card(i) for i in range(1, 5)])
        player1_hand = Hand([Card(i) for i in range(4, 8)])
        rest_card = Card(9)
        Deal(player0_hand, player1_hand, rest_card)
    except AssertionError as e:
        print(e)

    # Dealer ----------

    dealer = Dealer()

    deal = dealer.deal()
    print(deal.player0_hand.cards)
    print(deal.player1_hand.cards)
    print(deal.rest_card)

    deal = dealer.deal()
    print(deal.player0_hand.cards)
    print(deal.player1_hand.cards)
    print(deal.rest_card)
