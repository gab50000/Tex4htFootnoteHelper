#!/usr/bin/env python3

import sys
import re


# Name des HTML-Dokuments (mit den enthaltenen Markern)
# HTML_DOCUMENT = "VIII,2_Rahmen-TeX_11_modified.html"
HTML_DOCUMENT = "viii_test1_modified.html"


# Name des finalen HTML-Dokuments
# HTML_FINAL = "VIII,2_Rahmen-TeX_11_final.html"
HTML_FINAL = "viii_test1_final.html"


# Hier den Namen der Javascript Datei eintragen
JS_NAME = "footnotetest.js"


# Hier den Namen der css Datei eintragen
CSS_NAME = "footnotetest.css"


MODAL_STRING = r"""
<div id="modal-{id:}" class="modal">

    <!-- Modal content -->
    <div class="modal-content">
        <span class="close">x</span>
        <p>{content:}</p>
    </div>

</div>"""


FOOTNOTE_LINK_STRING = """
<a class="footnote-link" style="color:blue" id="footnote-link{counter:02d}">{content:}</a>
"""


def change_css_link(text, css_name):
    return re.sub(r"(?<=\<link\srel\=\"stylesheet\"\stype\=\"text\/css\"\shref\=\").*?(?=\")", 
                    css_name, text, flags=re.DOTALL)  #href="viii_modified.css" /> 


def insert_modal(text, index):
    search_string = r"""(\<[^\<\>]*?\>)?    # Last tag before footnote
                     \!\!FOOTNOTESTART\!\!  # Footnote marker
                     \({idx:}\)
                     (.*?)                  # Footnote content
                     \!\!FOOTNOTEEND\!\!    # Footnote end marker
                     (\<[^\<\>]*?\>)?       # First tag after footnote
                     """.format(idx=index)
                     
    modal_contents = re.findall(search_string, text, flags=re.DOTALL | re.VERBOSE)

    if len(modal_contents) != 1:
        print("Konnte Fußnote {} nicht finden".format(index))
        return text, None
    else:
        modal_content, = modal_contents
        modal_content = MODAL_STRING.format(id = str(index), content = "".join(modal_content))
                               # MODAL_STRING.format(id = str(index), content = r"\1\2\3"), 
        text_modified = re.sub(search_string, "", text,
                               flags=re.DOTALL | re.VERBOSE, count=1)
        return text_modified, modal_content
    

def insert_footnote_link(text, counter):
    search_string = r"""\!\!EDTEXTSTART\!\!  # Start tag
                     (.*?)                   # Edtext content
                     \!\!EDTEXTEND\!\!       # End tag
                     """
    text_modified = re.sub(search_string,
                           FOOTNOTE_LINK_STRING.format(counter=counter, content=r"{:02d}".format(counter)) + r" \1",
                           text,
                           flags=re.DOTALL | re.VERBOSE, count=1)
    return text_modified
    
    
def insert_modals_and_javascript(text, modals_list):
    modal_string = "\n".join(modals_list)
    text_modified = re.sub(r"(\<\/body\>)", 
                           r'{modal_string:}\n<script src="{js_name:}"></script>\n\1'.format(
                               modal_string=modal_string, js_name=JS_NAME), text)
    return text_modified


def insert_dummy_modals(modals_list):
    return [modal if modal else MODAL_STRING.format(id=i, content="Not found") \
            for i, modal in enumerate(modals_list)]


def check_that_all_footnotes_are_in_html(text):
    search_string = r"""(?:\<[^\<\>]*?\>)?     # Last tag before footnote
                        \!\!FOOTNOTESTART\!\!  # Footnote marker
                        \((\d+)\)              # Footnote number 
                        .*?                    # Footnote content
                        \!\!FOOTNOTEEND\!\!    # Footnote end marker
                        (?:\<[^\<\>]*?\>)?     # First tag after footnote
                        """
    numbers = [int(n) for n in re.findall(search_string, text, flags=re.VERBOSE | re.DOTALL)]
    all_numbers = set(range(1, max(numbers) + 1))
    missing_numbers = sorted(all_numbers - set(numbers))
    if missing_numbers:
        print("Folgende Fußnoten fehlen:", missing_numbers)
        return False
    else:
        print("Alle Fußnoten gefunden")
        return True



def main(*args):
    text = open(HTML_DOCUMENT, "r", encoding="iso-8859-1").read()
    if not check_that_all_footnotes_are_in_html(text):
        pass
    count = 1
    modals = []
    text = change_css_link(text, CSS_NAME)
    text_modified = insert_footnote_link(text, count)
    text_modified, modal = insert_modal(text_modified, count)
    modals.append(modal)
    while text_modified != text:
        count += 1
        text = text_modified
        text_modified = insert_footnote_link(text, count)
        text_modified, modal = insert_modal(text_modified, count)
        modals.append(modal)
    modals = insert_dummy_modals(modals)
    text_modified = insert_modals_and_javascript(text_modified, modals)
    with open(HTML_FINAL, "w", encoding="iso-8859-1") as f:
        print(text_modified, file=f)


if __name__ == "__main__":
    main()
