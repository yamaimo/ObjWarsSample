import random
from typing import NewType, Optional

# Card ====================

Card = NewType("Card", tuple[int])

CARD_MIN_NUMBER = 1
CARD_MAX_NUMBER = 9


def Card_init(number: int) -> Card:
    """
    カードを生成して返す
    不正な値の場合はAssertionError
    """
    assert (
        CARD_MIN_NUMBER <= number <= CARD_MAX_NUMBER
    ), f"Invalid number. (number: {number})"
    data = (number,)
    return Card(data)


def Card_get_number(card: Card) -> int:
    """カードの数字を返す"""
    return card[0]


def Card_get_all_cards() -> list[Card]:
    """すべてのカードを生成して返す"""
    return [Card_init(number) for number in range(CARD_MIN_NUMBER, CARD_MAX_NUMBER + 1)]


# Hand ====================

Hand = NewType("Hand", tuple[list[Card]])


def Hand_init(cards: list[Card]) -> Hand:
    """
    手札を生成して返す
    カードのリストが不正な場合はAssertionError
    """
    # 手札のチェック
    assert len(cards) == 4, f"The number of cards is invalid. (cards: {cards})"
    assert len(set(cards)) == 4, f"There are the same cards. (cards: {cards})"

    sorted_cards = sorted(cards, key=Card_get_number)
    data = (sorted_cards,)
    return Hand(data)


def Hand_get_cards(hand: Hand) -> list[Card]:
    """手札のカード一覧を返す"""
    return hand[0]


def Hand_has_card(hand: Hand, card: Card) -> bool:
    """手札に指定されたカードがあるか返す"""
    return card in hand[0]


# Deal ====================

Deal = NewType("Deal", tuple[Hand, Hand, Card])


def Deal_init(player0_hand: Hand, player1_hand: Hand, rest_card: Card) -> Deal:
    """
    ディールを生成して返す
    手札や残ったカードが不正な場合はAssertionError
    """
    # 使われてるカードのチェック
    used_card_set = set(
        Hand_get_cards(player0_hand) + Hand_get_cards(player1_hand) + [rest_card]
    )
    all_card_set = set(Card_get_all_cards())
    assert (
        used_card_set == all_card_set
    ), f"Card set is invalid. (used cards: {used_card_set})"

    data = (player0_hand, player1_hand, rest_card)
    return Deal(data)


def Deal_get_player0_hand(deal: Deal) -> Hand:
    """先手の手札を返す"""
    return deal[0]


def Deal_get_player1_hand(deal: Deal) -> Hand:
    """後手の手札を返す"""
    return deal[1]


def Deal_get_rest_card(deal: Deal) -> Card:
    """残ったカードを返す"""
    return deal[2]


# Dealer ====================

Dealer = NewType("Dealer", tuple[Optional[int]])


def Dealer_init(random_state: Optional[int] = None) -> Dealer:
    """ディーラーを生成して返す"""
    data = (random_state,)
    return Dealer(data)


def Dealer_deal(dealer: Dealer) -> Deal:
    """
    ディーラーにランダムにカードを配らせて
    ディールを生成して返す
    """
    random.seed(dealer[0])
    all_cards = Card_get_all_cards()
    shuffled_cards = random.sample(all_cards, len(all_cards))
    player0_hand = Hand_init(shuffled_cards[:4])
    player1_hand = Hand_init(shuffled_cards[4:8])
    rest_card = shuffled_cards[-1]
    return Deal_init(player0_hand, player1_hand, rest_card)


if __name__ == "__main__":
    # Card ----------

    all_cards = Card_get_all_cards()
    for card in all_cards:
        print(f"number: {Card_get_number(card)}")

    card1_1 = Card_init(1)
    card1_2 = Card_init(1)
    card2 = Card_init(2)
    assert card1_1 == card1_2
    assert card1_1 != card2
    assert card1_2 != card2

    try:
        Card_init(CARD_MIN_NUMBER - 1)
    except Exception as e:
        print(e)
    try:
        Card_init(CARD_MAX_NUMBER + 1)
    except Exception as e:
        print(e)

    # Hand ----------

    hand = Hand_init([Card_init(number) for number in range(1, 5)])
    print(Hand_get_cards(hand))
    print(Hand_has_card(hand, Card_init(1)))
    print(Hand_has_card(hand, Card_init(5)))

    try:
        Hand_init([Card_init(1), Card_init(2)])
    except AssertionError as e:
        print(e)
    try:
        Hand_init([Card_init(number) for number in [1, 2, 3, 1]])
    except AssertionError as e:
        print(e)

    # Deal ----------

    player0_hand = Hand_init([Card_init(i) for i in [1, 5, 7, 8]])
    player1_hand = Hand_init([Card_init(i) for i in [2, 4, 6, 9]])
    rest_card = Card_init(3)
    deal = Deal_init(player0_hand, player1_hand, rest_card)
    print(Hand_get_cards(Deal_get_player0_hand(deal)))
    print(Hand_get_cards(Deal_get_player1_hand(deal)))
    print(Deal_get_rest_card(deal))

    try:
        player0_hand = Hand_init([Card_init(i) for i in range(1, 5)])
        player1_hand = Hand_init([Card_init(i) for i in range(4, 8)])
        rest_card = Card_init(9)
        Deal_init(player0_hand, player1_hand, rest_card)
    except AssertionError as e:
        print(e)

    # Dealer ----------

    dealer = Dealer_init()

    deal = Dealer_deal(dealer)
    print(Hand_get_cards(Deal_get_player0_hand(deal)))
    print(Hand_get_cards(Deal_get_player1_hand(deal)))
    print(Deal_get_rest_card(deal))

    deal = Dealer_deal(dealer)
    print(Hand_get_cards(Deal_get_player0_hand(deal)))
    print(Hand_get_cards(Deal_get_player1_hand(deal)))
    print(Deal_get_rest_card(deal))
