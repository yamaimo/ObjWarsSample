from action import AskAction
from card import Card, Hand
from player import RandomAI
from smartai import SmartAI
from testtool import TestSubject

with TestSubject("SmartAI") as subject:
    hand = Hand([Card(number) for number in [1, 2, 3, 4]])

    @subject.testcase("init state.")
    def test_init_state() -> bool:
        ai = SmartAI("ai", hand, 0)

        rest_cards_expected = [Card(number) for number in [5, 6, 7, 8, 9]]
        bluff_cards_expected = [Card(number) for number in [1, 2, 3, 4]]

        if ai.rest_cards != rest_cards_expected:
            return False
        if ai.bluff_cards != bluff_cards_expected:
            return False
        if ai.maybe_card is not None:
            return False
        return True

    @subject.testcase("after asking.")
    def test_after_asking() -> bool:
        ai = SmartAI("ai", hand, 0)

        # AIが5を質問したケース
        ai.player_asked(ai, AskAction(Card(5)), True)

        # 5を質問したので質問してないカードから除かれる
        rest_cards_expected = [Card(number) for number in [6, 7, 8, 9]]
        bluff_cards_expected = [Card(number) for number in [1, 2, 3, 4]]

        if ai.rest_cards != rest_cards_expected:
            return False
        if ai.bluff_cards != bluff_cards_expected:
            return False
        if ai.maybe_card is not None:
            return False
        return True

    @subject.testcase("after bluffing.")
    def test_after_bluffing() -> bool:
        ai = SmartAI("ai", hand, 0)

        # AIが1をブラフしたケース
        ai.player_asked(ai, AskAction(Card(1)), False)

        # 1をブラフしたのでブラフに使えるカードから除かれる
        rest_cards_expected = [Card(number) for number in [5, 6, 7, 8, 9]]
        bluff_cards_expected = [Card(number) for number in [2, 3, 4]]

        if ai.rest_cards != rest_cards_expected:
            return False
        if ai.bluff_cards != bluff_cards_expected:
            return False
        if ai.maybe_card is not None:
            return False
        return True

    @subject.testcase("after asked (Hit).")
    def test_after_asked_hit() -> bool:
        ai = SmartAI("ai", hand, 0)
        opponent = RandomAI("opponent", 0)

        # AIが1を質問されたケース
        ai.player_asked(opponent, AskAction(Card(1)), True)

        # 1を質問されたのでブラフに使えるカードから除かれる
        rest_cards_expected = [Card(number) for number in [5, 6, 7, 8, 9]]
        bluff_cards_expected = [Card(number) for number in [2, 3, 4]]

        if ai.rest_cards != rest_cards_expected:
            return False
        if ai.bluff_cards != bluff_cards_expected:
            return False
        if ai.maybe_card is not None:
            return False
        return True

    @subject.testcase("after asked (Miss).")
    def test_after_asked_miss() -> bool:
        # AIが9を質問されたケースを考える
        # 確率で相手のブラフとして扱うときとそうでないときがある
        opponent = RandomAI("opponent", 0)

        # seedが0の場合、random.random()は0.84 -> 相手のブラフとして扱う
        ai = SmartAI("ai", hand, 0)
        ai.player_asked(opponent, AskAction(Card(9)), False)

        # 相手のブラフとして扱うので質問してないカードから除かれる
        rest_cards_expected = [Card(number) for number in [5, 6, 7, 8]]
        bluff_cards_expected = [Card(number) for number in [1, 2, 3, 4]]

        if ai.rest_cards != rest_cards_expected:
            return False
        if ai.bluff_cards != bluff_cards_expected:
            return False
        if ai.maybe_card is not None:
            return False

        # seedが1の場合、random.random()は0.13 -> 推測する
        ai = SmartAI("ai", hand, 1)
        ai.player_asked(opponent, AskAction(Card(9)), False)

        # 相手のブラフとして扱わないので推測候補にする
        rest_cards_expected = [Card(number) for number in [5, 6, 7, 8, 9]]
        bluff_cards_expected = [Card(number) for number in [1, 2, 3, 4]]

        if ai.rest_cards != rest_cards_expected:
            return False
        if ai.bluff_cards != bluff_cards_expected:
            return False
        if ai.maybe_card != Card(9):
            return False
        return True

    # 各状態での行動選択のテストは省略
