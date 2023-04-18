from io import StringIO

from terminal import Terminal
from testtool import TestSubject

with TestSubject("Terminal") as subject:

    @subject.testcase("get str.")
    def test_get_str() -> bool:
        in_stream = StringIO("test")
        out_stream = StringIO()
        terminal = Terminal(in_stream, out_stream)
        read = terminal.get_str("prompt")
        prompt = out_stream.getvalue()
        return (prompt == "prompt") and (read == "test")

    @subject.testcase("put str.")
    def test_put_str() -> bool:
        in_stream = StringIO()
        out_stream = StringIO()
        terminal = Terminal(in_stream, out_stream)
        terminal.put_str("test")
        output = out_stream.getvalue()
        return output == "test\n"

    @subject.testcase("put empty line.")
    def test_put_empty_line() -> bool:
        in_stream = StringIO()
        out_stream = StringIO()
        terminal = Terminal(in_stream, out_stream)
        terminal.put_empty_line()
        output = out_stream.getvalue()
        return output == "\n"
