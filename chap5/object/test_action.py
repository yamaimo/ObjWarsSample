from action import ActionList, AskAction, GuessAction
from card import Card, Hand
from testtool import TestSubject

with TestSubject("AskAction") as subject:
    action = AskAction(Card(1))

    @subject.testcase("get asked card.")
    def test_get_asked_card() -> bool:
        return action.card == Card(1)  # type: ignore

    @subject.testcase("ask representation.")
    def test_ask_repr() -> bool:
        return repr(action) == "Ask(Card(1))"

    @subject.testcase("ask equality.")
    def test_ask_equality() -> bool:
        same_ask = AskAction(Card(1))
        if action != same_ask:
            return False
        different_ask = AskAction(Card(2))
        if action == different_ask:
            return False
        guess = GuessAction(Card(1))
        if action == guess:
            return False
        return True

    @subject.testcase("check whether ask is hit.")
    def test_ask_is_hit() -> bool:
        opponent_hand = Hand(
            [Card(number) for number in range(1, 5)]
        )
        if not action.is_hit(opponent_hand):
            return False
        opponent_hand = Hand(
            [Card(number) for number in range(2, 6)]
        )
        if action.is_hit(opponent_hand):
            return False
        return True


with TestSubject("GuessAction") as subject:
    action = GuessAction(Card(1))

    @subject.testcase("get guessed card.")
    def test_get_guessed_card() -> bool:
        return action.card == Card(1)  # type: ignore

    @subject.testcase("guess representation.")
    def test_guess_repr() -> bool:
        return repr(action) == "Guess(Card(1))"

    @subject.testcase("guess equality.")
    def test_guess_equality() -> bool:
        same_guess = GuessAction(Card(1))
        if action != same_guess:
            return False
        different_guess = GuessAction(Card(2))
        if action == different_guess:
            return False
        ask = AskAction(Card(1))
        if action == ask:
            return False
        return True

    @subject.testcase("check whether guess is hit.")
    def test_guess_is_hit() -> bool:
        hit_card = Card(1)
        if not action.is_hit(hit_card):
            return False
        miss_card = Card(2)
        if action.is_hit(miss_card):
            return False
        return True


with TestSubject("ActionList") as subject:
    ask_actions = [
        AskAction(Card(number)) for number in range(1, 3)
    ]
    guess_actions = [
        GuessAction(Card(number)) for number in range(1, 4)
    ]
    action_list = ActionList(ask_actions, guess_actions)

    @subject.testcase("get ask actions.")
    def test_get_ask_actions() -> bool:
        expected = [AskAction(Card(1)), AskAction(Card(2))]
        return action_list.ask_actions == expected  # type: ignore

    @subject.testcase("get guess actions.")
    def test_get_guess_actions() -> bool:
        expected = [
            GuessAction(Card(1)),
            GuessAction(Card(2)),
            GuessAction(Card(3)),
        ]
        return action_list.guess_actions == expected  # type: ignore

    @subject.testcase("get all actions.")
    def test_get_all_actions() -> bool:
        expected = [
            AskAction(Card(1)),
            AskAction(Card(2)),
            GuessAction(Card(1)),
            GuessAction(Card(2)),
            GuessAction(Card(3)),
        ]
        return action_list.all_actions == expected  # type: ignore

    @subject.testcase("action list representation.")
    def test_action_list_repr() -> bool:
        expected = (
            "[Ask(Card(1)), Ask(Card(2)), "
            "Guess(Card(1)), Guess(Card(2)), "
            "Guess(Card(3))]"
        )
        return repr(action_list) == expected

    @subject.testcase("check whether list contains action.")
    def test_list_contains_action() -> bool:
        if AskAction(Card(1)) not in action_list:
            return False
        if AskAction(Card(3)) in action_list:
            return False
        if GuessAction(Card(1)) not in action_list:
            return False
        if GuessAction(Card(4)) in action_list:
            return False
        return True

    @subject.testcase("available actions (prev is None).")
    def test_get_available_actions_with_prev_None() -> bool:
        hand = Hand([Card(number) for number in range(1, 5)])
        prev_action = None
        available_actions = ActionList.get_available_actions(
            hand, prev_action
        )
        expected_all = [
            AskAction(Card(number)) for number in range(1, 10)
        ]
        return available_actions.all_actions == expected_all  # type: ignore  # noqa: B950

    @subject.testcase("available actions (prev is not None)")
    def test_get_available_actions_with_prev_not_None() -> bool:
        hand = Hand([Card(number) for number in range(1, 5)])
        prev_action = AskAction(Card(1))
        available_actions = ActionList.get_available_actions(
            hand, prev_action
        )
        expected_ask = [
            AskAction(Card(number)) for number in range(2, 10)
        ]
        expected_guess = [
            GuessAction(Card(number)) for number in range(5, 10)
        ]
        return (  # type: ignore
            available_actions.ask_actions == expected_ask
        ) and (
            available_actions.guess_actions == expected_guess
        )
