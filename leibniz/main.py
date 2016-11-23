import sys

import pexpect
import plac


def pdflatex(latex_file):
    """Run pdflatex without interruption"""
    child = pexpect.spawn("/usr/bin/pdflatex", [latex_file])
    child.logfile = sys.stdout
    child.expect_exact("?")
    child.sendline("R")


def main(*args):
    plac.call(pdflatex)


if __name__ == "__main__":
    main()
