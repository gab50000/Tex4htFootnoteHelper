import sys

import pexpect
import plac

from . import set_footnote_markers_in_tex
from . import find_all_footnotes_in_html


def pdflatex():
    """
    Call set_footnote_markers_in_tex,
    then run pdflatex without interruption.
    Finally, call find_all_footnotes_in_html"""
    
    latex_file = set_footnote_markers_in_tex.main()
    child = pexpect.spawn("/usr/bin/htlatex", [latex_file, "xhtml"])
    for i in range(3):
        child.expect_exact("?")
        child.sendline("R")
    print(child.read())
    find_all_footnotes_in_html.main()


def main(*args):
    plac.call(pdflatex)


if __name__ == "__main__":
    main()
