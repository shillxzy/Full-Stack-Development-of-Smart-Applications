"""Допоміжний запускач для run_all.py: виконує скрипт так, ніби дані вводяться
вручну, - кожне значення, прочитане input(), друкується після підказки."""
import builtins
import runpy
import sys

_input = builtins.input


def echo_input(prompt=""):
    print(prompt, end="")
    value = _input()
    print(value)
    return value


builtins.input = echo_input
script = sys.argv[1]
sys.argv = sys.argv[1:]
sys.path.insert(0, ".")
runpy.run_path(script, run_name="__main__")
