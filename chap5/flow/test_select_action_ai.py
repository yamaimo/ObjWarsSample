from contextlib import redirect_stdout
from io import StringIO

from guessit import get_available_actions, select_action_ai
from testtool import TestSubject

with TestSubject("select_action_ai()") as subject:

    @subject.testcase("select (prev action is None).")
    def test_select_with_prev_action_None() -> bool:
        # 標準出力を無視する
        with redirect_stdout(StringIO()):
            hand = [1, 2, 3, 4]
            prev_action = None
            selected = select_action_ai(hand, prev_action)
            available_actions = get_available_actions(hand, prev_action)
            return selected in available_actions

    @subject.testcase("select (prev action is not None).")
    def test_select_with_prev_action_not_None() -> bool:
        # 標準出力を無視する
        with redirect_stdout(StringIO()):
            hand = [1, 2, 3, 4]
            prev_action = {"kind": "ask", "card": 1}
            selected = select_action_ai(hand, prev_action)
            available_actions = get_available_actions(hand, prev_action)
            return selected in available_actions

    # handやprev_actionが不正な場合のテストは省略（本当は必要）
