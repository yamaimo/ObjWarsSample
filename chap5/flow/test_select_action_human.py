import sys
from io import StringIO
from typing import Optional

from guessit import Action, select_action_human
from testtool import TestSubject

with TestSubject("select_action_human()") as subject:

    @subject.testcase("print help (prev action is None).")
    def test_help_with_prev_action_None() -> bool:
        # 標準入出力を置き換えておく
        sys.stdin = StringIO("exit")
        sys.stdout = StringIO()
        try:
            hand = [1, 2, 3, 4]
            prev_action = None
            select_action_human(hand, prev_action)
        except Exception:
            pass
        finally:
            output = sys.stdout.getvalue()
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__
        ask_cards = list(range(1, 10))
        expected = (
            f"Your hand: {hand}\n"
            "Available commands:\n"
            f"  ask <card>      (<card>: {ask_cards})\n"
            "  exit\n"
            "player> "
        )
        return output == expected

    @subject.testcase("print help (prev action is not None).")
    def test_help_with_prev_action_not_None() -> bool:
        # 標準入出力を置き換えておく
        sys.stdin = StringIO("exit")
        sys.stdout = StringIO()
        try:
            hand = [1, 2, 3, 4]
            prev_action = {"kind": "ask", "card": 1}
            select_action_human(hand, prev_action)
        except Exception:
            pass
        finally:
            output = sys.stdout.getvalue()
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__
        ask_cards = list(range(2, 10))
        guess_cards = list(range(5, 10))
        expected = (
            f"Your hand: {hand}\n"
            "Available commands:\n"
            f"  ask <card>      (<card>: {ask_cards})\n"
            f"  guess <card>    (<card>: {guess_cards})\n"
            "  exit\n"
            "player> "
        )
        return output == expected

    @subject.testcase("ask.")
    def test_ask() -> bool:
        # 標準入出力を置き換えておく
        sys.stdin = StringIO("ask 1")
        sys.stdout = StringIO()
        try:
            hand = [1, 2, 3, 4]
            prev_action = None
            selected = select_action_human(hand, prev_action)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__
        expected = {"kind": "ask", "card": 1}
        return selected == expected

    @subject.testcase("guess.")
    def test_guess() -> bool:
        # 標準入出力を置き換えておく
        sys.stdin = StringIO("guess 1")
        sys.stdout = StringIO()
        try:
            hand = [5, 6, 7, 8]
            prev_action = {"kind": "ask", "card": 1}
            selected = select_action_human(hand, prev_action)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__
        expected = {"kind": "guess", "card": 1}
        return selected == expected

    @subject.testcase("exit.")
    def test_exit() -> bool:
        # 標準入出力を置き換えておく
        sys.stdin = StringIO("exit")
        sys.stdout = StringIO()
        try:
            hand = [1, 2, 3, 4]
            prev_action = None
            select_action_human(hand, prev_action)
            return False
        except Exception:
            pass
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__
        return True

    def test_error_message(
        command: str,
        error_message: str,
        hand: list[int] = [1, 2, 3, 4],  # noqa: B006
        prev_action: Optional[Action] = None,
    ) -> bool:
        # 標準入出力を置き換えておく
        sys.stdin = StringIO(f"{command}\nexit")
        sys.stdout = StringIO()
        try:
            select_action_human(hand, prev_action)
            return False
        except Exception:
            pass
        finally:
            output = sys.stdout.getvalue()
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__
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
        return test_error_message("ask 10", "Unavailable.")

    @subject.testcase("guess number is empty.")
    def test_guess_number_is_empty() -> bool:
        return test_error_message("guess", "Card is not specified.")

    @subject.testcase("guess number is invalid.")
    def test_guess_number_is_invalid() -> bool:
        return test_error_message("guess abc", "invalid literal for int()")

    @subject.testcase("guess number is out of range.")
    def test_guess_number_is_out_of_range() -> bool:
        return test_error_message("guess 10", "Unavailable.")

    @subject.testcase("action is not available.")
    def test_not_available_action() -> bool:
        return test_error_message("guess 1", "Unavailable.")

    # handやprev_actionが不正な場合のテストは省略（本当は必要）
