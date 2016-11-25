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
    
    
def find_next_edtext(text):
    match = re.search(r"\\edtext\{", text, flags=re.DOTALL)
    if match:
        _, position = match.span()
    else:
        return text,
    
    pre_edtext_content = text[:position]
    content, remaining = get_bracket_content(text[position:])
    if "edtext" in content:
        content = find_next_edtext(content)
    else:
        content = content,
        
    return (pre_edtext_content, "!!EDTEXTSTART!!") + content + ("!!EDTEXTEND!!",) + find_next_edtext(remaining)


class Insert:
    
    def __init__(self):
        self.counter = 1

    def insert_markers(self, text):
        subtexts = []
        remaining_text = text

        while True:
            match = re.search(r"\\edtext\{", remaining_text, flags=re.DOTALL)
            if match:
                _, position = match.span()
            else:
                break

            subtexts.append(remaining_text[:position])
            subtexts.append("!!EDTEXTSTART!!({:})".format(self.counter))
            content, remaining_text = get_bracket_content(remaining_text[position:])
            if "edtext" in content:
                pass
            subtexts.append(content)
            subtexts.append("!!EDTEXTEND!!}")
            remaining_text = remaining_text[1:]

            _, position = re.search(r"\\[ABC]footnote\{", remaining_text, flags=re.DOTALL).span()
            subtexts.append(remaining_text[:position])
            subtexts.append("!!FOOTNOTESTART!!({:})".format(self.counter))
            content, remaining_text = get_bracket_content(remaining_text[position:])
            subtexts.append(content)
            subtexts.append("!!FOOTNOTEEND!!")

            self.counter += 1

        subtexts.append(remaining_text)
        return "".join(subtexts)


def get_filename_modified(fname):
        fname_base, fname_ext = os.path.splitext(fname)
        fname_modified = fname_base + "_modified" + fname_ext
        return fname_modified


def get_text_without_comments(filename):
    with open(filename, "r") as f:
        text = f.readlines()
    return "".join([line for line in text if not line.lstrip().startswith("%")])


def main(*args):
    root_content = open(root_document, "r").read()
    insert = Insert()

    for tf in tex_files:
        print("Markiere footnotes in", tf)
        directory, filename = os.path.split(tf)
        fname_modified = get_filename_modified(filename)
        text = get_text_without_comments(tf)
        modified = find_next_edtext(text)
        text_modified = "".join(modified)
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

