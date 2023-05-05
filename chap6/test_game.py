from io import StringIO

from action import Action, ActionList, AskAction, GuessAction
from card import Card, Deal, Hand
from game import Game, GameObserver, GameView
from player import Player
from terminal import Terminal
from testtool import TestSubject


class ScenarioPlayer(Player):  # type: ignore
    def __init__(self, name: str, actions: list[Action]) -> None:
        self.__name = name
        self.__actions = actions

    @property
    def name(self) -> str:
        return self.__name

    def select_action(self, available_actions: ActionList) -> Action:
        action = self.__actions.pop(0)
        assert action in available_actions, f"Unavailable action. (action: {action})"
        return action


class NotifyChecker(GameObserver):  # type: ignore
    def __init__(self) -> None:
        self.__players: list[Player] = []
        self.__actions: list[Action] = []
        self.__judges: list[bool] = []

    @property
    def notify_count(self) -> int:
        return len(self.__players)

    def get_notify(self, i: int) -> tuple[Player, Action, bool]:
        return self.__players[i], self.__actions[i], self.__judges[i]

    def player_asked(self, player: Player, ask: AskAction, is_hit: bool) -> None:
        self.__players.append(player)
        self.__actions.append(ask)
        self.__judges.append(is_hit)

    def player_guessed(self, player: Player, guess: GuessAction, is_hit: bool) -> None:
        self.__players.append(player)
        self.__actions.append(guess)
        self.__judges.append(is_hit)


with TestSubject("Game") as subject:
    player0_hand = Hand([Card(number) for number in [1, 2, 3, 4]])
    player1_hand = Hand([Card(number) for number in [5, 6, 7, 8]])
    rest_card = Card(9)
    deal = Deal(player0_hand, player1_hand, rest_card)

    @subject.testcase("test scenario 1.")
    def test_scenario1() -> bool:
        player0 = ScenarioPlayer("player0", [AskAction(Card(1))])
        player1 = ScenarioPlayer("player1", [GuessAction(Card(1))])
        game = Game(deal, player0, player1)
        checker = NotifyChecker()
        game.add_observer(checker)

        win_player = game.start()

        if checker.notify_count != 2:
            return False

        player, action, is_hit = checker.get_notify(0)
        if (player != player0) or (action != AskAction(Card(1))) or is_hit:
            return False

        player, action, is_hit = checker.get_notify(1)
        if (player != player1) or (action != GuessAction(Card(1))) or is_hit:
            return False

        return win_player == player0  # type: ignore

    @subject.testcase("test scenario 2.")
    def test_scenario2() -> bool:
        player0 = ScenarioPlayer("player0", [AskAction(Card(5))])
        player1 = ScenarioPlayer("player1", [GuessAction(Card(9))])
        game = Game(deal, player0, player1)
        checker = NotifyChecker()
        game.add_observer(checker)

        win_player = game.start()

        if checker.notify_count != 2:
            return False

        player, action, is_hit = checker.get_notify(0)
        if (player != player0) or (action != AskAction(Card(5))) or (not is_hit):
            return False

        player, action, is_hit = checker.get_notify(1)
        if (player != player1) or (action != GuessAction(Card(9))) or (not is_hit):
            return False

        return win_player == player1  # type: ignore

    @subject.testcase("test scenario 3.")
    def test_scenario3() -> bool:
        player0 = ScenarioPlayer("player0", [AskAction(Card(1)), GuessAction(Card(5))])
        player1 = ScenarioPlayer("player1", [AskAction(Card(5))])
        game = Game(deal, player0, player1)
        checker = NotifyChecker()
        game.add_observer(checker)

        win_player = game.start()

        if checker.notify_count != 3:
            return False

        player, action, is_hit = checker.get_notify(0)
        if (player != player0) or (action != AskAction(Card(1))) or is_hit:
            return False

        player, action, is_hit = checker.get_notify(1)
        if (player != player1) or (action != AskAction(Card(5))) or is_hit:
            return False

        player, action, is_hit = checker.get_notify(2)
        if (player != player0) or (action != GuessAction(Card(5))) or is_hit:
            return False

        return win_player == player1  # type: ignore

    @subject.testcase("test scenario 4.")
    def test_scenario4() -> bool:
        player0 = ScenarioPlayer("player0", [AskAction(Card(5)), GuessAction(Card(9))])
        player1 = ScenarioPlayer("player1", [AskAction(Card(1))])
        game = Game(deal, player0, player1)
        checker = NotifyChecker()
        game.add_observer(checker)

        win_player = game.start()

        if checker.notify_count != 3:
            return False

        player, action, is_hit = checker.get_notify(0)
        if (player != player0) or (action != AskAction(Card(5))) or (not is_hit):
            return False

        player, action, is_hit = checker.get_notify(1)
        if (player != player1) or (action != AskAction(Card(1))) or (not is_hit):
            return False

        player, action, is_hit = checker.get_notify(2)
        if (player != player0) or (action != GuessAction(Card(9))) or (not is_hit):
            return False

        return win_player == player0  # type: ignore

    @subject.testcase("not notify to removed observer.")
    def test_remove_observer() -> bool:
        player0 = ScenarioPlayer("player0", [AskAction(Card(1))])
        player1 = ScenarioPlayer("player1", [GuessAction(Card(2))])
        game = Game(deal, player0, player1)

        checker1 = NotifyChecker()
        game.add_observer(checker1)
        checker2 = NotifyChecker()
        game.add_observer(checker2)
        game.remove_observer(checker1)

        game.start()

        return (checker1.notify_count == 0) and (checker2.notify_count == 2)


with TestSubject("GameView") as subject:

    @subject.testcase("test output.")
    def test_output() -> bool:
        player = ScenarioPlayer("test", [])
        out_stream = StringIO()
        terminal = Terminal(out_stream=out_stream)
        view = GameView(terminal)
        view.player_asked(player, AskAction(Card(1)), True)
        view.player_asked(player, AskAction(Card(2)), False)
        view.player_guessed(player, GuessAction(Card(1)), True)
        view.player_guessed(player, GuessAction(Card(2)), False)
        output = out_stream.getvalue()
        expected = (
            "test: Ask(Card(1))\n"
            "Hit.\n"
            "\n"
            "test: Ask(Card(2))\n"
            "Miss.\n"
            "\n"
            "test: Guess(Card(1))\n"
            "Hit.\n"
            "\n"
            "test: Guess(Card(2))\n"
            "Miss.\n"
            "\n"
        )
        return output == expected
