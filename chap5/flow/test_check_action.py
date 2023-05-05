from contextlib import redirect_stdout
from io import StringIO

from guessit import check_action
from testtool import TestSubject

with TestSubject("check_action()") as subject:

    @subject.testcase("player0 ask and hit.")
    def test_player0_ask_and_hit() -> bool:
        player = 0
        action = {"kind": "ask", "card": 1}
        opponent_hand = [1, 2, 3, 4]
        rest_card = 9
        # 出力をキャプチャ
        with redirect_stdout(StringIO()) as f:
            win_player = check_action(player, action, opponent_hand, rest_card)
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
            win_player = check_action(player, action, opponent_hand, rest_card)
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
            win_player = check_action(player, action, opponent_hand, rest_card)
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
            win_player = check_action(player, action, opponent_hand, rest_card)
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
            win_player = check_action(player, action, opponent_hand, rest_card)
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
            win_player = check_action(player, action, opponent_hand, rest_card)
            output = f.getvalue()
            return (win_player == 0) and (output == "Miss.\n\n")

    # playerが0/1以外だった場合、
    # actionが不正だった場合、
    # opponent_handが不正だった場合、
    # rest_cardが不正だった場合、
    # それぞれについて本当はテストが必要だが省略
