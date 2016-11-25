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
    
    print("Set footnote markers")
    latex_file = set_footnote_markers_in_tex.main()
    print("Compile Latex to HTML")
    child = pexpect.spawn("/usr/bin/htlatex", [latex_file, "xhtml"], timeout=300)
    for i in range(3):
        child.expect_exact("?")
        child.sendline("R")
    print(child.read())
    child.close()
    print("Modify HTML")
    find_all_footnotes_in_html.main()


def main(*args):
    plac.call(pdflatex)


if __name__ == "__main__":
    main()
