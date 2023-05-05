# ObjWarsSample

同人誌『オブジェクト・ウォーズ』のサンプルコード。

## エピソード1: 試練の始まり

題材とするゲーム『ゲス・イット』のルール説明（コードなし）。

## エピソード2: フローの追跡

処理の流れに注目して書いたコード。

```
- chap2/
    - guessit.py
        - ゲーム対戦のプログラム
```

## エピソード3: オブジェクトの覚醒

オブジェクトに注目して書いたコード。

```
- chap3/
    - __init__.py
    - card.py
        - カード、手札、ディール、ディーラーの実装
    - action.py
        - 質問、推測、行動、行動の一覧の実装
    - terminal.py
        - ターミナルの実装
    - player.py
        - 人のプレイヤー、ランダム選択のAI、プレイヤーの実装
    - game.py
        - ゲームの実装
    - guessit.py
        - ゲーム対戦のプログラム
```

## エピソード4: クラスの導き

クラスを使って書き直したコード。

```
- chap4/
    - __init__.py
    - card.py
        - カード、手札、ディール、ディーラーの実装（クラス）
    - action.py
        - 質問、推測、行動、行動の一覧の実装（クラス）
    - terminal.py
        - ターミナルの実装（クラス）
    - player.py
        - 人のプレイヤー、ランダム選択のAI、プレイヤーの実装（クラス）
    - game.py
        - ゲームの実装（クラス）
    - guessit.py
        - ゲーム対戦のプログラム
```

## エピソード5: テストへの挑戦

単体テストの作成。

```
- chap5/flow/
    - __init__.py
    - guessit.py@
    - testtool.py
        - シンプルなテストツール
    - test_deal.py
        - 手札の分配のテスト
    - test_get_available_actions.py
        - 可能な行動一覧の取得のテスト
    - test_select_action_human.py
        - 人の行動選択のテスト
    - test_select_action_ai.py
        - ランダムAIの行動選択のテスト
    - test_check_action.py
        - 行動判定のテスト
    - test_start_game.py
        - ゲーム進行のテスト
    - test_show_result.py
        - 結果表示のテスト
    - test_all.sh
        - 一連のテストを実行するshellスクリプト
- chap5/object/
    - __init__.py@
    - testtool.py@
    - card.py@
    - action.py@
    - terminal.py@
    - player.py@
    - game.py@
    - test_card.py
        - カード、手札、ディール、ディーラーのテスト
    - test_action.py
        - 質問、推測、行動、行動の一覧のテスト
    - test_terminal.py
        - ターミナルのテスト
    - test_player.py
        - 人のプレイヤー、ランダム選択のAI、プレイヤーのテスト
    - test_game.py
        - ゲームのテスト
    - test_all.sh
        - 一連のテストを実行するshellスクリプト
```

## エピソード6: 柔軟な繋がりの獲得

インタフェースの導入、責務の分離。

```
- chap6/
    - __init__.py@
    - testtool.py@
    - card.py@
    - action.py@
    - terminal.py@
    - player.py
        - Playerプロトコルを追加
    - game.py
        - GameObserverプロトコルを追加、ゲームからビューを分離
    - guessit.py
    - test_game.py
        - ゲーム、ビューのテスト
```

## エピソード7: 変化への適応

賢いAIの導入、対戦成績の調査。

```
- chap7/
    - __init__.py@
    - testtool.py@
    - card.py@
    - action.py@
    - terminal.py@
    - player.py@
    - game.py@
    - smartai.py
        - 賢いAIの実装
    - guessit.py
    - guessit_battle_ai.py
        - AI同士を対戦させるプログラム
    - test_smartai.py
        - 賢いAIのテスト
```

## エピソード8: 継承か委譲か

継承と委譲に関する議論（コードなし）。

## エピソード9: デザインの夜明け

発展的な話題の案内（コードなし）。
