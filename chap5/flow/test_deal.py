from guessit import deal
from testtool import TestSubject

with TestSubject("deal()") as subject:
    player0_hand, player1_hand, rest_card = deal()

    @subject.testcase("player0_hand size is 4.")
    def test_player0_hand_size() -> bool:
        return len(player0_hand) == 4

    @subject.testcase("player1_hand size is 4.")
    def test_player1_hand_size() -> bool:
        return len(player1_hand) == 4

    @subject.testcase("deal is valid.")
    def test_deal_is_valid() -> bool:
        rest_numbers = list(range(1, 10))
        for number in player0_hand:
            if number not in rest_numbers:
                return False
            rest_numbers.remove(number)
        for number in player1_hand:
            if number not in rest_numbers:
                return False
            rest_numbers.remove(number)
        if len(rest_numbers) != 1:
            return False
        return rest_card == rest_numbers[0]
