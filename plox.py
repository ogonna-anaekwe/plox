from _interpreter import Interpreter
from _parser import Parser
from _scanner import Scanner
import argparse
import sys


class Plox:
    """Entry point for plox interpreter."""

    def __init__(self):
        # same interpreter for all ASTS in batch or interactive mode.
        self.interpreter = Interpreter()

    def run(self, src):
        """Runs source code."""
        tokens = Scanner(src).scan()
        asts = Parser(tokens).parse()
        self.interpreter.interpret(asts)

    def run_file(self, src_fp):
        """Runs code (top to bottom) in batch mode directly from a file."""
        try:
            with open(src_fp) as f:
                self.run(f.read())
        except Exception:
            raise

    def start_repl(self):
        """Starts REPL to run code in interactive mode."""
        print(
            ">> you're in the plox REPL. to exit: either type exit and hit return or ctrl + c <<"
        )
        while True:
            print(">>", end=" ")  # " " means accept user input on same line as >>
            user_input = input()
            exit_repl = user_input.strip() == "exit"
            if exit_repl:
                break

            try:
                self.run(user_input)
            except Exception as e:
                # do not kill REPL when exceptions are raised.
                print(e)


if __name__ == "__main__":
    sys.tracebacklimit = 0  # Print only last line in error stack trace.
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-s",
        type=str,
        required=False,
        help="path to file containing the source code you want to interpret.",
    )

    namespace_dict = vars(arg_parser.parse_args())
    src_file_path = namespace_dict.get("s")
    plox = Plox()
    plox.start_repl() if src_file_path is None else plox.run_file(src_file_path)
