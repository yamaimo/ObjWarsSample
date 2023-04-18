# シンプルなテストツール

from typing import Callable

TestFunc = Callable[[], bool]
TestRunner = Callable[[TestFunc], None]


class TestSubject:
    def __init__(self, subject: str) -> None:
        self.__subject = subject
        self.__results: list[bool] = []

    def __enter__(self) -> "TestSubject":
        print(f"Test {self.__subject} ====================")
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore  # noqa: B950
        ok_count = sum(self.__results)
        total_count = len(self.__results)
        if total_count == 0:
            result = "Nothing"
        elif ok_count < total_count:
            result = "Failure"
        else:
            result = "Success"
        print(f"{result}. ({ok_count}/{total_count})")

    def testcase(self, description: str) -> TestRunner:
        def test_runner(test_func: TestFunc) -> None:
            print(f"{description} ... ", end="", flush=True)
            result = test_func()
            self.__results.append(result)
            print("OK" if result else "NG")

        return test_runner


if __name__ == "__main__":
    with TestSubject("Hoge") as subject:

        @subject.testcase("hoge")
        def hoge() -> bool:
            return True

        @subject.testcase("huga")
        def huga() -> bool:
            return False

    with TestSubject("Huga") as subject:

        @subject.testcase("xxx")
        def xxx() -> bool:
            return True

        @subject.testcase("yyy")
        def yyy() -> bool:
            return True
