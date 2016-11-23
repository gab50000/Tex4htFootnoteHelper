import sys

import pexpect
import plac


def pdflatex(latex_file):
    """Run pdflatex without interruption"""
    child = pexpect.spawn("/usr/bin/pdflatex", [latex_file])
    # child.logfile = sys.stdout
    child.expect_exact("?")
    child.sendline("R")
    print(child.before.decode("utf-8"))
    print(child.after.decode("utf-8"))


def main(*args):
    plac.call(pdflatex)


if __name__ == "__main__":
    main()
