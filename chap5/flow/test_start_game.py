from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from guessit import start_game
from testtool import TestSubject

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
