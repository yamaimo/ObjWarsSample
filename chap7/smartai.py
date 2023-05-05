import random
from typing import Optional

from action import Action, ActionList, AskAction, GuessAction
from card import Card, Hand
from game import GameObserver
from player import Player


class SmartAI(Player, GameObserver):  # type: ignore
    def __init__(
        self, name: str, hand: Hand, random_state: Optional[int] = None
    ) -> None:
        self.__name = name
        self.__hand = hand
        self.__random_state = random_state

        # 伏せられたカードの候補
        self.__rest_cards: list[Card] = []
        # ブラフに使えるカードの一覧
        self.__bluff_cards: list[Card] = []
        # 次に推測するカード
        self.__maybe_card: Optional[Card] = None

        self.__init_state()

    def __init_state(self) -> None:
        self.__rest_cards = [
            card for card in Card.get_all_cards() if not self.__hand.has_card(card)
        ]
        self.__bluff_cards = list(self.__hand.cards)
        self.__maybe_card = None
        random.seed(self.__random_state)

    @property
    def name(self) -> str:
        """プレイヤーの名前を返す"""
        return self.__name

    # テスト用
    @property
    def rest_cards(self) -> list[Card]:
        return self.__rest_cards

    # テスト用
    @property
    def bluff_cards(self) -> list[Card]:
        return self.__bluff_cards

    # テスト用
    @property
    def maybe_card(self) -> Optional[Card]:
        return self.__maybe_card

    def select_action(self, available_actions: ActionList) -> Action:
        """
        AIに行動を選択させて返す
        以下のアルゴリズムで選択する：
        1. 伏せられたカードの候補が1枚、
           もしくは次に推測するカードがあるなら推測する
        2. そうでない場合、推測可能なら確率で推測する
        3. 推測しない場合、可能なら確率でブラフする
        4. ブラフしない場合、単に質問する
        """
        selected: Action = (
            self.__guess_with_maybe_card()
            or self.__may_guess(available_actions.guess_actions)
            or self.__may_bluff()
            or self.__ask()
        )
        assert selected in available_actions, (
            "Invalid action. "
            f"(action: {selected}, "
            f"available: {available_actions})"
        )
        return selected

    def __guess_with_maybe_card(self) -> Optional[GuessAction]:
        guess: Optional[GuessAction] = None
        if len(self.__rest_cards) == 1:
            guess = GuessAction(self.__rest_cards[0])
        elif self.__maybe_card is not None:
            guess = GuessAction(self.__maybe_card)
        return guess

    def __may_guess(self, guess_actions: list[GuessAction]) -> Optional[GuessAction]:
        guess: Optional[GuessAction] = None
        if guess_actions:
            if self.__rest_cards:
                guess_th = 1 / len(self.__rest_cards)
                if random.random() <= guess_th:
                    selected_card = random.choice(self.__rest_cards)
                    guess = GuessAction(selected_card)
            else:
                # 相手のブラフと判断したカードがブラフではなく、
                # しかし相手がそのカードを推測しなかった場合、
                # 伏せられたカードの候補がなくなることがある
                # この場合はランダムに推測する
                guess = random.choice(guess_actions)
        return guess

    def __may_bluff(self) -> Optional[AskAction]:
        bluff: Optional[AskAction] = None
        if self.__bluff_cards:
            # 4枚: 5%, 3枚: 10%, 2枚: 15%, 1枚: 20%
            bluff_th = (5 - len(self.__bluff_cards)) / 20
            if random.random() <= bluff_th:
                selected_card = random.choice(self.__bluff_cards)
                bluff = AskAction(selected_card)
        return bluff

    def __ask(self) -> AskAction:
        selected_card = random.choice(self.__rest_cards)
        return AskAction(selected_card)

    def player_asked(self, player: Player, ask: AskAction, is_hit: bool) -> None:
        """プレイヤーが質問したときに実行される"""
        # 自分が質問したときは、
        # 1. ブラフならブラフに使えるカードから除外
        # 2. 質問なら伏せられたカードの候補から除外
        #    そしてヒットしなかったら相手の手札にないので
        #    次に推測するカードとする
        # そうでない場合、
        # 1. まず質問されたカードはブラフに使えなくなる
        # 2. そしてヒットしなかった場合それは
        #    a. 相手のブラフ（相手の手札にある）
        #    b. 伏せられたカード
        #    のいずれかなので、確率で次の手を考える
        if player == self:
            if ask.card in self.__bluff_cards:
                self.__bluff_cards.remove(ask.card)
            else:
                self.__rest_cards.remove(ask.card)
                if not is_hit:
                    self.__maybe_card = ask.card
        else:
            if ask.card in self.__bluff_cards:
                self.__bluff_cards.remove(ask.card)
            if not is_hit:
                # 伏せられたカードの候補に入っていないなら
                # すでに質問してヒットしたカードなので
                # 確実にブラフ -> 無視する
                if ask.card not in self.__rest_cards:
                    pass
                else:
                    # 伏せられたカードの候補が多いときの方が
                    # たまたま当たった可能性は低い
                    # （＝ブラフの可能性高い）
                    not_bluff_th = 1 / len(self.__rest_cards)
                    if random.random() <= not_bluff_th:
                        self.__maybe_card = ask.card
                    else:
                        self.__rest_cards.remove(ask.card)

    def player_guessed(self, player: Player, guess: GuessAction, is_hit: bool) -> None:
        """プレイヤーが推測したときに実行される"""
        # 同じゲームをできるように初期化しておく
        self.__init_state()
