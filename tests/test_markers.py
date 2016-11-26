import unittest

from leibniz import set_footnote_markers_in_tex as sfmit

class TestFootnoteMarkers(unittest.TestCase):
    
    def test_find_next_environment(self):
        test_string = r"Blablablub\edtext{Some content with {more {} brackets {{}} inside}}"
        pre, marker1, content, marker2, rest = sfmit.find_next_environment(r"edtext", "edtext", test_string)
        self.assertEqual(content, r"Some content with {more {} brackets {{}} inside}")
        self.assertEqual(pre, r"Blablablub\edtext{")
        self.assertEqual(rest, r"}")
        
    def test_Enumerator(self):
        test_string = r"Blablablub\edtext{!!EDTEXTSTART!!Some content with {more {} brackets {{}} inside}!!EDTEXTEND!!}" \
                      "\lemma{abc}\Afootnote{hallo}"
        ed_enum = sfmit.Enumerator(r"!!EDTEXTSTART!!")
        result = ed_enum.enumerate_markers(test_string)
        print(result)
        self.assertTrue(r"!!EDTEXTSTART!!(01)Some content with {more {} brackets {{}} inside}!!EDTEXTEND!!" in result)
        
    def test_nested_edtexts(self):
        test_string = r"""Blablablub\edtext{Some content with {more {} brackets \edtext{and another
edtext }\lemma{edtext}\Cfootnote{deep inside} {{}} inside}}\lemma{abc}\Afootnote{hallo}"""
        
