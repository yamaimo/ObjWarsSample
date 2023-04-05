import sys
from typing import NewType, TextIO

# Terminal ====================

Terminal = NewType("Terminal", tuple[TextIO, TextIO])


def Terminal_init(
    in_stream: TextIO = sys.stdin,
    out_stream: TextIO = sys.stdout,
) -> Terminal:
    """ターミナルを生成して返す"""
    data = (in_stream, out_stream)
    return Terminal(data)


def Terminal_get_str(terminal: Terminal, prompt: str) -> str:
    """
    プロンプトを表示し、
    入力された文字列を1行読み取って返す
    """
    terminal[1].write(prompt)
    terminal[1].flush()
    return terminal[0].readline()


def Terminal_put_str(terminal: Terminal, output: str) -> None:
    """文字列を出力する"""
    terminal[1].write(output)
    terminal[1].write("\n")
    terminal[1].flush()


def Terminal_put_empty_line(terminal: Terminal) -> None:
    """空行を出力する"""
    terminal[1].write("\n")
    terminal[1].flush()


if __name__ == "__main__":
    from io import StringIO

    terminal = Terminal_init()
    string = Terminal_get_str(terminal, "input> ")
    Terminal_put_str(terminal, string)
    Terminal_put_empty_line(terminal)

    with StringIO("test") as in_stream:
        with StringIO() as out_stream:
            terminal = Terminal_init(in_stream, out_stream)
            string = Terminal_get_str(terminal, "input> ")
            Terminal_put_str(terminal, string)
            output = out_stream.getvalue()
    print(output)
