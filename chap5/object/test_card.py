from card import Card, Deal, Dealer, Hand
from testtool import TestSubject

with TestSubject("Card") as subject:
    card = Card(5)

    @subject.testcase("card number.")
    def test_card_number() -> bool:
        return card.number == 5  # type: ignore

    @subject.testcase("card representation.")
    def test_card_repr() -> bool:
        return repr(card) == "Card(5)"

    @subject.testcase("card hash value.")
    def test_card_hash() -> bool:
        return hash(card) == hash(5)

    @subject.testcase("card equality.")
    def test_card_equality() -> bool:
        same_card = Card(5)
        if card != same_card:
            return False
        different_card = Card(6)
        if card == different_card:
            return False
        return True

    @subject.testcase("card order.")
    def test_card_order() -> bool:
        lower_card = Card(4)
        higher_card = Card(6)
        if lower_card > card:
            return False
        if higher_card < card:
            return False
        return True

    @subject.testcase("invalid number is not allowed.")
    def test_invalid_number() -> bool:
        try:
            Card(0)
            return False
        except Exception:
            pass
        try:
            Card(10)
            return False
        except Exception:
            pass
        return True

    @subject.testcase("get all cards.")
    def test_get_all_cards() -> bool:
        all_cards = Card.get_all_cards()
        expected = [Card(number) for number in range(1, 10)]
        return all_cards == expected  # type: ignore


with TestSubject("Hand") as subject:
    cards = [Card(number) for number in range(1, 5)]
    hand = Hand(cards)

    @subject.testcase("get cards.")
    def test_cards() -> bool:
        cards = hand.cards
        expected = [Card(number) for number in range(1, 5)]
        return cards == expected  # type: ignore

    @subject.testcase("check whether hand has card.")
    def test_hand_has_card() -> bool:
        has_numbers = [1, 2, 3, 4]
        not_has_numbers = [5, 6, 7, 8, 9]
        for number in has_numbers:
            if not hand.has_card(Card(number)):
                return False
        for number in not_has_numbers:
            if hand.has_card(Card(number)):
                return False
        return True

    @subject.testcase("invalid card count is not allowed.")
    def test_invalid_card_count() -> bool:
        cards = [Card(number) for number in range(1, 3)]
        try:
            Hand(cards)
            return False
        except Exception:
            return True

    @subject.testcase("duplicated cards are not allowed.")
    def test_duplicated_cards() -> bool:
        cards = [Card(1), Card(2), Card(3), Card(1)]
        try:
            Hand(cards)
            return False
        except Exception:
            return True


with TestSubject("Deal") as subject:
    player0_hand = Hand(
        [Card(number) for number in range(1, 5)]
    )
    player1_hand = Hand(
        [Card(number) for number in range(5, 9)]
    )
    rest_card = Card(9)
    deal = Deal(player0_hand, player1_hand, rest_card)

    @subject.testcase("get player0 hand.")
    def test_player0_hand() -> bool:
        player0_hand_cards = deal.player0_hand.cards
        expected = [Card(number) for number in range(1, 5)]
        return player0_hand_cards == expected  # type: ignore

    @subject.testcase("get player1 hand.")
    def test_player1_hand() -> bool:
        player1_hand_cards = deal.player1_hand.cards
        expected = [Card(number) for number in range(5, 9)]
        return player1_hand_cards == expected  # type: ignore

    @subject.testcase("get rest card.")
    def test_rest_card() -> bool:
        rest_card = deal.rest_card
        expected = Card(9)
        return rest_card == expected  # type: ignore

    @subject.testcase("overlapped hands are not allowed.")
    def test_overlapped_hands() -> bool:
        player0_hand = Hand(
            [Card(number) for number in range(1, 5)]
        )
        player1_hand = Hand(
            [Card(number) for number in range(4, 8)]
        )
        rest_card = Card(9)
        try:
            Deal(player0_hand, player1_hand, rest_card)
            return False
        except Exception:
            return True

    @subject.testcase("rest card must not be in hands.")
    def test_rest_card_in_hands() -> bool:
        player0_hand = Hand(
            [Card(number) for number in range(1, 5)]
        )
        player1_hand = Hand(
            [Card(number) for number in range(5, 9)]
        )
        try:
            rest_card = Card(1)
            Deal(player0_hand, player1_hand, rest_card)
            return False
        except Exception:
            pass
        try:
            rest_card = Card(8)
            Deal(player0_hand, player1_hand, rest_card)
            return False
        except Exception:
            pass
        return True


with TestSubject("Dealer") as subject:

    @subject.testcase("deal randomly.")
    def test_deal_randomly() -> bool:
        dealer = Dealer()
        deal1 = dealer.deal()
        deal2 = dealer.deal()
        # たまたま同じになってしまう可能性はあるが、
        # 低いと考えられる
        if deal1.player0_hand.cards != deal2.player0_hand.cards:
            return True
        if deal1.player1_hand.cards != deal2.player1_hand.cards:
            return True
        return False

    @subject.testcase("deal with fixed seed.")
    def test_deal_with_fixed_seed() -> bool:
        dealer = Dealer(0)
        deal1 = dealer.deal()
        deal2 = dealer.deal()
        # シードが同じなので同じ配り方になる
        if deal1.player0_hand.cards != deal2.player0_hand.cards:
            return False
        if deal1.player1_hand.cards != deal2.player1_hand.cards:
            return False
        return True
