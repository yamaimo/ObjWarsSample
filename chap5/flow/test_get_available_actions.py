from guessit import get_available_actions
from testtool import TestSubject

with TestSubject("get_available_actions()") as subject:

    @subject.testcase("prev action is None case.")
    def test_prev_action_is_None() -> bool:
        hand = [1, 2, 3, 4]
        prev_action = None
        available_actions = get_available_actions(hand, prev_action)
        expected = [{"kind": "ask", "card": card} for card in range(1, 10)]
        return available_actions == expected

    @subject.testcase("prev action is not None case.")
    def test_prev_action_is_not_None() -> bool:
        hand = [1, 2, 3, 4]
        prev_action = {"kind": "ask", "card": 1}
        available_actions = get_available_actions(hand, prev_action)
        expected = [{"kind": "ask", "card": card} for card in range(2, 10)]
        expected += [{"kind": "guess", "card": card} for card in range(5, 10)]
        return available_actions == expected

    @subject.testcase("hand number is invalid case.")
    def test_hand_number_is_invalid() -> bool:
        try:
            hand = [-1, 2, 3, 4]
            prev_action = None
            get_available_actions(hand, prev_action)
            return False
        except Exception:
            return True

    @subject.testcase("hand is empty case.")
    def test_hand_is_empty() -> bool:
        try:
            hand: list[int] = []
            prev_action = None
            get_available_actions(hand, prev_action)
            return False
        except Exception:
            return True

    @subject.testcase("prev action is invalid case.")
    def test_prev_action_is_invalid() -> bool:
        try:
            hand = [1, 2, 3, 4]
            prev_action = {"abc": 123}
            get_available_actions(hand, prev_action)
            return False
        except Exception:
            return True
