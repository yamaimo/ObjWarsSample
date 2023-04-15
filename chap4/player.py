import random
from typing import Optional, Union

from action import Action, ActionList, AskAction, GuessAction
from card import Card, Hand
from terminal import Terminal


class HumanPlayer:
    def __init__(
        self, name: str, hand: Hand, terminal: Terminal
    ) -> None:
        """人のプレイヤーを初期化する"""
        self.__name = name
        self.__hand = hand
        self.__terminal = terminal

    @property
    def name(self) -> str:
        """人のプレイヤーの名前を返す"""
        return self.__name

    def select_action(
        self, available_actions: ActionList
    ) -> Action:
        while True:
            self.__print_help(available_actions)

            command, args = self.__get_command()
            if command is None:
                self.__terminal.put_str("Empty Command.")
                self.__terminal.put_empty_line()
                continue

            action = self.__parse_command(command, args)
            if action is None:
                self.__terminal.put_str("Parse Error.")
                self.__terminal.put_empty_line()
                continue
            if action not in available_actions:
                self.__terminal.put_str(
                    f"Unavailable. (action: {action})",
                )
                self.__terminal.put_empty_line()
                continue

            return action

    def __print_help(
        self,
        available_actions: ActionList,
    ) -> None:
        hand_str = self.__format_cards(self.__hand.cards)
        self.__terminal.put_str(f"Your hand: {hand_str}")

        self.__terminal.put_str("Available commands:")

        ask_cards = [
            action.card
            for action in available_actions.ask_actions
        ]
        ask_str = self.__format_cards(ask_cards)
        if ask_str:
            ask_help = f"  ask <card>      (<card>: {ask_str})"
            self.__terminal.put_str(ask_help)

        guess_cards = [
            action.card
            for action in available_actions.guess_actions
        ]
        guess_str = self.__format_cards(guess_cards)
        if guess_str:
            guess_help = (
                f"  guess <card>    (<card>: {guess_str})"
            )
            self.__terminal.put_str(guess_help)

        self.__terminal.put_str("  exit")

    def __format_cards(self, cards: list[Card]) -> str:
        card_numbers = [card.number for card in cards]
        return ", ".join(map(str, card_numbers))

    def __get_command(self) -> tuple[Optional[str], list[str]]:
        input_str = self.__terminal.get_str(f"{self.__name}> ")
        args = input_str.strip().split()
        if len(args) < 1:
            return None, []
        command = args.pop(0).lower()
        return command, args

    def __parse_command(
        self, command: str, args: list[str]
    ) -> Optional[Action]:
        if command == "exit":
            raise Exception("Exit game.")

        if command not in ["ask", "guess"]:
            self.__terminal.put_str(
                f"Unknown Command. (command: {command})",
            )
            return None

        if len(args) < 1:
            self.__terminal.put_str("Card is not specified.")
            return None

        try:
            card = Card(int(args[0]))
        except Exception as e:
            self.__terminal.put_str(str(e))
            return None

        if command == "ask":
            action = AskAction(card)
        else:
            action = GuessAction(card)

        return action


class RandomAI:
    def __init__(
        self, name: str, random_state: Optional[int] = None
    ) -> None:
        """ランダム選択のAIを初期化する"""
        random.seed(random_state)
        self.__name = name

    @property
    def name(self) -> str:
        """AIの名前を返す"""
        return self.__name

    def select_action(
        self, available_actions: ActionList
    ) -> Action:
        """行動をAIにランダムに選択させて返す"""
        return random.choice(available_actions.all_actions)


Player = Union[HumanPlayer, RandomAI]


if __name__ == "__main__":
    from io import StringIO

    from card import Dealer
    from terminal import Terminal

    deal = Dealer(0).deal()
    hand = deal.player0_hand

    terminal = Terminal(in_stream=StringIO("ask 1\nguess 2\n"))

    # HumanPlayer
    human = HumanPlayer("human", hand, terminal)

    available_actions = ActionList.get_available_actions(
        hand, None
    )
    action = human.select_action(available_actions)
    print(f"{human.name} select {action}")
    print()

    available_actions = ActionList.get_available_actions(
        hand, action
    )
    action = human.select_action(available_actions)
    print(f"{human.name} select {action}")
    print()

    # RandomAI
    rand_ai = RandomAI("random", 0)

    available_actions = ActionList.get_available_actions(
        hand, None
    )
    action = rand_ai.select_action(available_actions)
    print(f"{rand_ai.name} select {action}")
    print()

    available_actions = ActionList.get_available_actions(
        hand, action
    )
    action = rand_ai.select_action(available_actions)
    print(f"{rand_ai.name} select {action}")
    print()
