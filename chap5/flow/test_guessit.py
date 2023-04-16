import sys
from contextlib import redirect_stdout
from io import StringIO
from typing import Optional
from unittest.mock import patch

from guessit import (
    Action,
    check_action,
    deal,
    get_available_actions,
    select_action_ai,
    select_action_human,
    show_result,
    start_game,
)
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


with TestSubject("get_available_actions()") as subject:

    @subject.testcase("prev action is None case.")
    def test_prev_action_is_None() -> bool:
        hand = [1, 2, 3, 4]
        prev_action = None
        available_actions = get_available_actions(
            hand, prev_action
        )
        expected = [
            {"kind": "ask", "card": card}
            for card in range(1, 10)
        ]
        return available_actions == expected

    @subject.testcase("prev action is not None case.")
    def test_prev_action_is_not_None() -> bool:
        hand = [1, 2, 3, 4]
        prev_action = {"kind": "ask", "card": 1}
        available_actions = get_available_actions(
            hand, prev_action
        )
        expected = [
            {"kind": "ask", "card": card}
            for card in range(2, 10)
        ]
        expected += [
            {"kind": "guess", "card": card}
            for card in range(5, 10)
        ]
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
            action = select_action_human(hand, prev_action)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__
        expected = {"kind": "ask", "card": 1}
        return action == expected

    @subject.testcase("guess.")
    def test_guess() -> bool:
        # 標準入出力を置き換えておく
        sys.stdin = StringIO("guess 1")
        sys.stdout = StringIO()
        try:
            hand = [5, 6, 7, 8]
            prev_action = {"kind": "ask", "card": 1}
            action = select_action_human(hand, prev_action)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__
        expected = {"kind": "guess", "card": 1}
        return action == expected

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
        return test_error_message(
            "dummy", "Unknown Command. (command: dummy)"
        )

    @subject.testcase("ask number is empty.")
    def test_ask_number_is_empty() -> bool:
        return test_error_message(
            "ask", "Card is not specified."
        )

    @subject.testcase("ask number is invalid.")
    def test_ask_number_is_invalid() -> bool:
        return test_error_message(
            "ask abc", "invalid literal for int()"
        )

    @subject.testcase("ask number is out of range.")
    def test_ask_number_is_out_of_range() -> bool:
        return test_error_message("ask 10", "Unavailable.")

    @subject.testcase("guess number is empty.")
    def test_guess_number_is_empty() -> bool:
        return test_error_message(
            "guess", "Card is not specified."
        )

    @subject.testcase("guess number is invalid.")
    def test_guess_number_is_invalid() -> bool:
        return test_error_message(
            "guess abc", "invalid literal for int()"
        )

    @subject.testcase("guess number is out of range.")
    def test_guess_number_is_out_of_range() -> bool:
        return test_error_message("guess 10", "Unavailable.")

    @subject.testcase("action is not available.")
    def test_not_available_action() -> bool:
        return test_error_message("guess 1", "Unavailable.")

    # handやprev_actionが不正な場合のテストは省略（本当は必要）


with TestSubject("select_action_ai()") as subject:

    @subject.testcase("print help (prev action is None).")
    def test_select_with_prev_action_None() -> bool:
        # 標準出力を無視する
        with redirect_stdout(StringIO()):
            hand = [1, 2, 3, 4]
            prev_action = None
            action = select_action_ai(hand, prev_action)
            available_actions = get_available_actions(
                hand, prev_action
            )
            return action in available_actions

    @subject.testcase("print help (prev action is not None).")
    def test_select_with_prev_action_not_None() -> bool:
        # 標準出力を無視する
        with redirect_stdout(StringIO()):
            hand = [1, 2, 3, 4]
            prev_action = {"kind": "ask", "card": 1}
            action = select_action_ai(hand, prev_action)
            available_actions = get_available_actions(
                hand, prev_action
            )
            return action in available_actions

    # handやprev_actionが不正な場合のテストは省略（本当は必要）


with TestSubject("check_action()") as subject:

    @subject.testcase("player0 ask and hit.")
    def test_player0_ask_and_hit() -> bool:
        player = 0
        action = {"kind": "ask", "card": 1}
        opponent_hand = [1, 2, 3, 4]
        rest_card = 9
        # 出力をキャプチャ
        with redirect_stdout(StringIO()) as f:
            win_player = check_action(
                player, action, opponent_hand, rest_card
            )
            if win_player is not None:
                return False
            output = f.getvalue()
            return output == "Hit.\n\n"

    @subject.testcase("player0 ask and miss.")
    def test_player0_ask_and_miss() -> bool:
        player = 0
        action = {"kind": "ask", "card": 1}
        opponent_hand = [5, 6, 7, 9]
        rest_card = 9
        # 出力をキャプチャ
        with redirect_stdout(StringIO()) as f:
            win_player = check_action(
                player, action, opponent_hand, rest_card
            )
            if win_player is not None:
                return False
            output = f.getvalue()
            return output == "Miss.\n\n"

    @subject.testcase("player0 guess and hit.")
    def test_player0_guess_and_hit() -> bool:
        player = 0
        action = {"kind": "guess", "card": 1}
        opponent_hand = [5, 6, 7, 8]
        rest_card = 1
        # 出力をキャプチャ
        with redirect_stdout(StringIO()) as f:
            win_player = check_action(
                player, action, opponent_hand, rest_card
            )
            output = f.getvalue()
            return (win_player == 0) and (output == "Hit.\n\n")

    @subject.testcase("player0 guess and miss.")
    def test_player0_guess_and_miss() -> bool:
        player = 0
        action = {"kind": "guess", "card": 1}
        opponent_hand = [1, 2, 3, 4]
        rest_card = 9
        # 出力をキャプチャ
        with redirect_stdout(StringIO()) as f:
            win_player = check_action(
                player, action, opponent_hand, rest_card
            )
            output = f.getvalue()
            return (win_player == 1) and (output == "Miss.\n\n")

    @subject.testcase("player1 guess and hit.")
    def test_player1_guess_and_hit() -> bool:
        player = 1
        action = {"kind": "guess", "card": 1}
        opponent_hand = [5, 6, 7, 8]
        rest_card = 1
        # 出力をキャプチャ
        with redirect_stdout(StringIO()) as f:
            win_player = check_action(
                player, action, opponent_hand, rest_card
            )
            output = f.getvalue()
            return (win_player == 1) and (output == "Hit.\n\n")

    @subject.testcase("player1 guess and miss.")
    def test_player1_guess_and_miss() -> bool:
        player = 1
        action = {"kind": "guess", "card": 1}
        opponent_hand = [1, 2, 3, 4]
        rest_card = 9
        # 出力をキャプチャ
        with redirect_stdout(StringIO()) as f:
            win_player = check_action(
                player, action, opponent_hand, rest_card
            )
            output = f.getvalue()
            return (win_player == 0) and (output == "Miss.\n\n")

    # playerが0/1以外だった場合、
    # actionが不正だった場合、
    # opponent_handが不正だった場合、
    # rest_cardが不正だった場合、
    # それぞれについて本当はテストが必要だが省略


with TestSubject("start_game()") as subject:
    # テストが難しい
    # unittest.mock.patchで頑張る手はある
    @subject.testcase("use mock.")
    def test_with_mock() -> bool:
        with patch("guessit.select_action_human") as human_mock:
            with patch("guessit.select_action_ai") as ai_mock:
                with redirect_stdout(StringIO()):
                    human_mock.return_value = {
                        "kind": "ask",
                        "card": 1,
                    }
                    ai_mock.return_value = {
                        "kind": "guess",
                        "card": 1,
                    }
                    player0_hand = [1, 2, 3, 4]
                    player1_hand = [5, 6, 7, 8]
                    rest_card = 9
                    win_player = start_game(
                        player0_hand, player1_hand, rest_card
                    )
                    return win_player == 0

    # 他のパターンも考えられるが省略


with TestSubject("show_result()") as subject:

    @subject.testcase("player0 won.")
    def test_player0_won() -> bool:
        with redirect_stdout(StringIO()) as f:
            show_result(0)
            output = f.getvalue()
            expected = "You won.\n"
            return output == expected

    @subject.testcase("player1 won.")
    def test_player1_won() -> bool:
        with redirect_stdout(StringIO()) as f:
            show_result(1)
            output = f.getvalue()
            expected = "You lost.\n"
            return output == expected

    @subject.testcase("invalid player won.")
    def test_invalid_player_won() -> bool:
        with redirect_stdout(StringIO()):
            try:
                show_result(2)
                return False
            except Exception:
                return True
