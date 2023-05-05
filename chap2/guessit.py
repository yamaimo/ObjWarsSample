import random
from typing import Any, Optional

Action = dict[str, Any]


def deal() -> tuple[list[int], list[int], int]:
    """
    各プレイヤーに手札を配る
    - 入力: なし
    - 出力1: 先手の手札（整数のリスト）
    - 出力2: 後手の手札（整数のリスト）
    - 出力3: 残りのカード（整数）
    """
    all_cards = list(range(1, 10))
    shuffled_cards = random.sample(all_cards, len(all_cards))
    player0_hand = sorted(shuffled_cards[:4])
    player1_hand = sorted(shuffled_cards[4:8])
    rest_card = shuffled_cards[-1]
    return player0_hand, player1_hand, rest_card


def get_available_actions(
    hand: list[int], prev_action: Optional[Action]
) -> list[Action]:
    """
    可能な行動一覧
    - 入力1: 手番プレイヤーの手札（整数のリスト）
    - 入力2: 直前の行動（辞書／なし）
    - 出力: 可能な行動一覧（辞書のリスト）
    """
    actions = [{"kind": "ask", "card": card} for card in range(1, 10)]

    if prev_action is not None:
        actions.remove(prev_action)
        for card in range(1, 10):
            if card not in hand:
                actions.append({"kind": "guess", "card": card})

    return actions


def select_action_human(hand: list[int], prev_action: Optional[Action]) -> Action:
    """
    人の場合の行動選択
    - 入力1: 手番プレイヤーの手札（整数のリスト）
    - 入力2: 直前の行動（辞書／なし）
    - 出力: 選択した行動（辞書）
    """
    available_actions = get_available_actions(hand, prev_action)
    ask_cards = []
    guess_cards = []
    for action in available_actions:
        if action["kind"] == "ask":
            ask_cards.append(action["card"])
        else:
            guess_cards.append(action["card"])

    while True:
        print(f"Your hand: {hand}")
        print("Available commands:")
        if ask_cards:
            print(f"  ask <card>      (<card>: {ask_cards})")
        if guess_cards:
            print(f"  guess <card>    (<card>: {guess_cards})")
        print("  exit")

        args = input("player> ").strip().split()
        if len(args) < 1:
            print("Empty Command.")
            print()  # 一行空ける
            continue

        command = args[0].lower()
        card: Optional[int] = None
        if len(args) >= 2:
            try:
                card = int(args[1])
            except ValueError as e:
                print(e)
                print()  # 一行空ける
                continue

        if command == "ask":
            if card is None:
                print("Card is not specified.")
                print()  # 一行空ける
                continue
            action = {"kind": "ask", "card": card}
        elif command == "guess":
            if card is None:
                print("Card is not specified.")
                print()  # 一行空ける
                continue
            action = {"kind": "guess", "card": card}
        elif command == "exit":
            raise Exception("Exit game.")
        else:
            print(f"Unknown Command. (command: {command})")
            print()  # 一行空ける
            continue

        if action not in available_actions:
            print(f"Unavailable. (action: {action})")
            print()  # 一行空ける
            continue
        else:
            print(f"You select {action}")
            return action


def select_action_ai(hand: list[int], prev_action: Optional[Action]) -> Action:
    """
    AIの場合の行動選択
    - 入力1: 手番プレイヤーの手札（整数のリスト）
    - 入力2: 直前の行動（辞書／なし）
    - 出力: 選択した行動（辞書）
    """
    available_actions = get_available_actions(hand, prev_action)
    action = random.choice(available_actions)
    print(f"AI select {action}")
    return action


def check_action(
    player: int, action: Action, opponent_hand: list[int], rest_card: int
) -> Optional[int]:
    """
    選択された行動を判定
    - 入力1: 先手番か後手番か（整数）
    - 入力2: 選択された行動（辞書）
    - 入力3: 相手の手札（整数のリスト）
    - 入力4: 残りのカード（整数）
    - 出力: 勝った手番（整数／なし）
    """
    win_player = None

    if action["kind"] == "ask":
        if action["card"] in opponent_hand:
            print("Hit.")
        else:
            print("Miss.")
    else:
        if action["card"] == rest_card:
            print("Hit.")
            win_player = player
        else:
            print("Miss.")
            opponent_player = (player + 1) % 2  # 0->1, 1->0
            win_player = opponent_player
    print()  # 一行空ける

    return win_player


def start_game(player0_hand: list[int], player1_hand: list[int], rest_card: int) -> int:
    """
    ゲームを進行する
    - 入力1: 先手の手札（整数のリスト）
    - 入力2: 後手の手札（整数のリスト）
    - 入力3: 残りのカード（整数）
    - 出力: 勝った手番（整数）
    """
    turn_player = 0

    prev_action: Optional[Action] = None
    while True:
        if turn_player == 0:
            action = select_action_human(player0_hand, prev_action)
            win_player = check_action(0, action, player1_hand, rest_card)
        else:
            action = select_action_ai(player1_hand, prev_action)
            win_player = check_action(1, action, player0_hand, rest_card)

        if win_player is not None:
            return win_player

        prev_action = action
        turn_player = (turn_player + 1) % 2  # 0->1, 1->0


def show_result(win_player: int) -> None:
    """
    ゲーム結果を伝える
    - 入力: 勝った手番（整数）
    - 出力: なし
    """
    if win_player == 0:
        print("You won.")
    else:
        print("You lost.")


def main() -> None:
    """メイン"""
    player0_hand, player1_hand, rest_card = deal()
    win_player = start_game(player0_hand, player1_hand, rest_card)
    show_result(win_player)


if __name__ == "__main__":
    main()
