from io import StringIO
from typing import Optional

from action import ActionList, AskAction, GuessAction
from card import Card, Hand
from player import HumanPlayer, RandomAI
from terminal import Terminal
from testtool import TestSubject

with TestSubject("HumanPlayer") as subject:
    name = "Human"
    hand = Hand([Card(number) for number in range(1, 5)])

    @subject.testcase("get human name.")
    def test_get_human_name() -> bool:
        terminal = Terminal()
        player = HumanPlayer(name, hand, terminal)
        return player.name == "Human"  # type: ignore

    @subject.testcase("print help (guess is empty).")
    def test_help_with_no_guess() -> bool:
        in_stream = StringIO("exit")
        out_stream = StringIO()
        terminal = Terminal(in_stream, out_stream)
        player = HumanPlayer(name, hand, terminal)
        prev_action = None
        available_actions = ActionList.get_available_actions(hand, prev_action)
        try:
            player.select_action(available_actions)
        except Exception:
            pass
        output = out_stream.getvalue()
        hand_cards = ", ".join(map(str, range(1, 5)))
        ask_cards = ", ".join(map(str, range(1, 10)))
        expected = (
            f"Your hand: {hand_cards}\n"
            "Available commands:\n"
            f"  ask <card>      (<card>: {ask_cards})\n"
            "  exit\n"
            f"{name}> "
        )
        return output == expected

    @subject.testcase("print help (guess is not empty).")
    def test_help_with_guess() -> bool:
        in_stream = StringIO("exit")
        out_stream = StringIO()
        terminal = Terminal(in_stream, out_stream)
        player = HumanPlayer(name, hand, terminal)
        prev_action = AskAction(Card(1))
        available_actions = ActionList.get_available_actions(hand, prev_action)
        try:
            player.select_action(available_actions)
        except Exception:
            pass
        output = out_stream.getvalue()
        hand_cards = ", ".join(map(str, range(1, 5)))
        ask_cards = ", ".join(map(str, range(2, 10)))
        guess_cards = ", ".join(map(str, range(5, 10)))
        expected = (
            f"Your hand: {hand_cards}\n"
            "Available commands:\n"
            f"  ask <card>      (<card>: {ask_cards})\n"
            f"  guess <card>    (<card>: {guess_cards})\n"
            "  exit\n"
            f"{name}> "
        )
        return output == expected

    @subject.testcase("ask.")
    def test_ask() -> bool:
        in_stream = StringIO("ask 1")
        out_stream = StringIO()
        terminal = Terminal(in_stream, out_stream)
        player = HumanPlayer(name, hand, terminal)
        prev_action = None
        available_actions = ActionList.get_available_actions(hand, prev_action)
        selected = player.select_action(available_actions)
        expected = AskAction(Card(1))
        return selected == expected  # type: ignore

    @subject.testcase("guess.")
    def test_guess() -> bool:
        in_stream = StringIO("guess 5")
        out_stream = StringIO()
        terminal = Terminal(in_stream, out_stream)
        player = HumanPlayer(name, hand, terminal)
        prev_action = AskAction(Card(1))
        available_actions = ActionList.get_available_actions(hand, prev_action)
        selected = player.select_action(available_actions)
        expected = GuessAction(Card(5))
        return selected == expected  # type: ignore

    @subject.testcase("exit.")
    def test_exit() -> bool:
        in_stream = StringIO("exit")
        out_stream = StringIO()
        terminal = Terminal(in_stream, out_stream)
        player = HumanPlayer(name, hand, terminal)
        prev_action = None
        available_actions = ActionList.get_available_actions(hand, prev_action)
        try:
            player.select_action(available_actions)
            return False
        except Exception:
            return True

    def test_error_message(
        command: str,
        error_message: str,
        hand: Hand = hand,
        prev_action: Optional[AskAction] = None,
    ) -> bool:
        in_stream = StringIO(f"{command}\nexit")
        out_stream = StringIO()
        terminal = Terminal(in_stream, out_stream)
        player = HumanPlayer(name, hand, terminal)
        available_actions = ActionList.get_available_actions(hand, prev_action)
        try:
            player.select_action(available_actions)
            return False
        except Exception:
            pass
        output = out_stream.getvalue()
        lines = output.split("\n")
        for line in lines:
            if error_message in line:
                return True
        return False

    @subject.testcase("empty command.")
    def test_empty_command() -> bool:
        return test_error_message("", "Empty Command.")

    @subject.testcase("unknown command.")
    def test_unknown_command() -> bool:
        return test_error_message("dummy", "Unknown Command. (command: dummy)")

    @subject.testcase("ask number is empty.")
    def test_ask_number_is_empty() -> bool:
        return test_error_message("ask", "Card is not specified.")

    @subject.testcase("ask number is invalid.")
    def test_ask_number_is_invalid() -> bool:
        return test_error_message("ask abc", "invalid literal for int()")

    @subject.testcase("ask number is out of range.")
    def test_ask_number_is_out_of_range() -> bool:
        return test_error_message("ask 10", "Invalid number. (number: 10)")

    @subject.testcase("guess number is empty.")
    def test_guess_number_is_empty() -> bool:
        return test_error_message("guess", "Card is not specified.")

    @subject.testcase("guess number is invalid.")
    def test_guess_number_is_invalid() -> bool:
        return test_error_message("guess abc", "invalid literal for int()")

    @subject.testcase("guess number is out of range.")
    def test_guess_number_is_out_of_range() -> bool:
        return test_error_message("guess 10", "Invalid number. (number: 10)")

    @subject.testcase("action is not available.")
    def test_not_available_action() -> bool:
        return test_error_message("guess 1", "Unavailable.")


with TestSubject("RandomAI") as subject:
    name = "AI"
    hand = Hand([Card(number) for number in range(1, 5)])

    @subject.testcase("get ai name.")
    def test_get_ai_name() -> bool:
        player = RandomAI(name)
        return player.name == "AI"  # type: ignore

    @subject.testcase("select (prev action is None).")
    def test_select_with_prev_action_None() -> bool:
        player = RandomAI(name)
        prev_action = None
        available_actions = ActionList.get_available_actions(hand, prev_action)
        selected = player.select_action(available_actions)
        return selected in available_actions

    @subject.testcase("select (prev action is not None).")
    def test_select_with_prev_action_not_None() -> bool:
        player = RandomAI(name)
        prev_action = AskAction(Card(1))
        available_actions = ActionList.get_available_actions(hand, prev_action)
        selected = player.select_action(available_actions)
        return selected in available_actions
