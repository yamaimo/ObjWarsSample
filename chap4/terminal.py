import sys
from typing import TextIO


class Terminal:
    def __init__(
        self, in_stream: TextIO = sys.stdin, out_stream: TextIO = sys.stdout
    ) -> None:
        """ターミナルを初期化する"""
        self.__in_stream = in_stream
        self.__out_stream = out_stream

    def get_str(self, prompt: str) -> str:
        """
        プロンプトを表示し、
        入力された文字列を1行読み取って返す
        """
        self.__out_stream.write(prompt)
        self.__out_stream.flush()
        return self.__in_stream.readline()

    def put_str(self, output: str) -> None:
        """文字列を出力する"""
        self.__out_stream.write(output)
        self.__out_stream.write("\n")
        self.__out_stream.flush()

    def put_empty_line(self) -> None:
        """空行を出力する"""
        self.__out_stream.write("\n")
        self.__out_stream.flush()


if __name__ == "__main__":
    from io import StringIO

    terminal = Terminal()
    string = terminal.get_str("input> ").strip()
    terminal.put_str(f"input string: {string}")
    terminal.put_str("---")
    terminal.put_empty_line()
    terminal.put_str("---")

    with StringIO("test") as in_stream:
        with StringIO() as out_stream:
            terminal = Terminal(in_stream, out_stream)
            string = terminal.get_str("input> ").strip()
            terminal.put_str(f"input string: {string}")
            output = out_stream.getvalue()
    print("--output--")
    print(output)
