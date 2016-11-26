#!/usr/bin/env python3

import os
import re


tex_files = [
    "gesamttex/edit/LH037_05_010r.tex",
    "gesamttex/edit/LH037_05_010v.tex",
    "gesamttex/edit/LH037_05_011rspez.tex",
    "gesamttex/edit/LH037_05_011v.tex",
    "gesamttex/edit/LH037_05_006r.tex",
    "gesamttex/edit/LH037_05_006v.tex"]

# Hier Namen (und ggf. Verzeichnis) des Latex Root Dokuments angeben

# root_document = "VIII,2_Rahmen-TeX_11.tex"
root_document = "viii_test1.tex"


def get_bracket_content(text):
    open_braces = 1
    start_position, position = 0, 0
    
    while True:
        subtext = text[position:]
        next_lbracket_index, next_rbracket_index = subtext.find("{"), subtext.find("}")

        if next_lbracket_index < next_rbracket_index:
            if next_lbracket_index == -1:
                if next_rbracket_index == -1:
                    print("uh oh")
                else:
                    next_bracket_index = next_rbracket_index
            else:
                next_bracket_index = next_lbracket_index
        elif next_rbracket_index == -1:
            next_bracket_index = next_lbracket_index
        else:
            next_bracket_index = next_rbracket_index

        next_bracket = subtext[next_bracket_index]
        if next_bracket == "}":
            open_braces -= 1
        else:
            open_braces += 1
        position += next_bracket_index + 1
        if open_braces == 0:
            break
    return text[start_position: position-1], text[position-1:]
    
    
def find_next_environment(search_string, name, text):
    expr = r"\\%s\{" % search_string
    start_marker = "!!%sSTART!!" % name.upper()
    end_marker = "!!%sEND!!" % name.upper()
    match = re.search(expr, text, flags=re.DOTALL)
    if match:
        _, position = match.span()
    else:
        return text,
    
    pre_edtext_content = text[:position]
    content, remaining = get_bracket_content(text[position:])
    if name in content:
        content = find_next_environment(search_string, name, content)
    else:
        content = content,
        
    return (pre_edtext_content, start_marker) + content + (end_marker,) \
            + find_next_environment(search_string, name, remaining)


def get_filename_modified(fname):
        fname_base, fname_ext = os.path.splitext(fname)
        fname_modified = fname_base + "_modified" + fname_ext
        return fname_modified


def get_text_without_comments(filename):
    with open(filename, "r") as f:
        text = f.readlines()
    return "".join([line for line in text if not line.lstrip().startswith("%")])

class Enumerator:

    def __init__(self, expr):
        self.counter = 1
        self.expr = expr

    def enumerate_markers(self, text):
        matches = re.finditer(self.expr, text)
        indices = [0]
        for m in matches:
            indices.append(m.span()[1])

        modified = []

        for i, (start, end) in enumerate(zip(indices[:-1], indices[1:]), self.counter):
            modified.append(text[start:end])
            modified.append("({:02d})".format(i))
        self.counter = i + 1
        return "".join(modified)


def main(*args):
    root_content = open(root_document, "r").read()
    fn_enumerator = Enumerator(r"!!FOOTNOTESTART!!")
    ed_enumerator = Enumerator(r"!!EDTEXTSTART!!")

    for tf in tex_files:
        print("Markiere footnotes in", tf)
        directory, filename = os.path.split(tf)
        fname_modified = get_filename_modified(filename)
        text = get_text_without_comments(tf)
        modified = find_next_environment(r"edtext", "edtext", text)
        text_modified = "".join(modified)
        modified = find_next_environment(r"[ABC]footnote", "footnote", text_modified)
        text_modified = "".join(modified)
        text_modified = fn_enumerator.enumerate_markers(text_modified)
        text_modified = ed_enumerator.enumerate_markers(text_modified)
        root_content = re.sub(re.escape(filename), fname_modified, root_content)
        filepath_modified = os.path.join(directory, fname_modified)
        print("Modifizierte Version wird gespeichert in", filepath_modified)
        with open(filepath_modified, "w") as f:
            f.write(text_modified)
    fpath_modified = get_filename_modified(root_document)
    print("Speichere modifiziertes Root Dokument mit Verweisen zu den modifizierten Tex-Dateien "
          "nach", fpath_modified)
    with open(fpath_modified, "w") as f:
        f.write(root_content)
        
    return fpath_modified


if __name__ == "__main__":
    main()

