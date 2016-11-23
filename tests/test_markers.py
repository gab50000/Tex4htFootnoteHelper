import unittest

from leibniz import set_footnote_markers_in_tex as sfmit

class TestFootnoteMarkers(unittest.TestCase):
    
    def test_find_next_edtext(self):
        test_string = r"Blablablub\edtext{Some content with {more {} brackets {{}} inside}}"
        pre, content, rest = sfmit.find_next_edtext(test_string)
        self.assertEqual(content, r"Some content with {more {} brackets {{}} inside}")
        self.assertEqual(pre, r"Blablablub\edtext{")
        self.assertEqual(rest, r"}")
        
    def test_Insert(self):
        test_string = r"Blablablub\edtext{Some content with {more {} brackets {{}} inside}}" \
                      "\lemma{abc}\Afootnote{hallo}"
        insert = sfmit.Insert()
        result = insert.insert_markers(test_string)
        print(result)
        self.assertTrue(r"!!EDTEXTSTART!!(1)Some content with {more {} brackets {{}} inside}!!EDTEXTEND!!" in result)
        
    def test_nested_edtexts(self):
        test_string = r"""Blablablub\edtext{Some content with {more {} brackets \edtext{and another
edtext }\lemma{edtext}\Cfootnote{deep inside} {{}} inside}}\lemma{abc}\Afootnote{hallo}"""
        
