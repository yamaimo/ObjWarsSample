from contextlib import redirect_stdout
from io import StringIO

from guessit import show_result
from testtool import TestSubject

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
