import sys
from typing import NewType, TextIO

# Terminal ====================

Terminal = NewType("Terminal", tuple[TextIO, TextIO])


def Terminal_init(
    in_stream: TextIO = sys.stdin,
    out_stream: TextIO = sys.stdout,
) -> Terminal:
    data = (in_stream, out_stream)
    return Terminal(data)


def Terminal_get_str(terminal: Terminal, prompt: str) -> str:
    terminal[1].write(prompt)
    terminal[1].flush()
    return terminal[0].readline()


def Terminal_put_str(terminal: Terminal, output: str) -> None:
    terminal[1].write(output)
    terminal[1].write("\n")
    terminal[1].flush()


def Terminal_put_empty_line(terminal: Terminal) -> None:
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
