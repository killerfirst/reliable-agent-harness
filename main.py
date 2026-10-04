import sys

from dotenv import load_dotenv

from harness.loop import run_agent


load_dotenv()


def main():
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        task = """
        Fix the bug in this project so that all tests pass.
        Do not modify the tests.
        """

    run_agent(task)


if __name__ == "__main__":
    main()
    