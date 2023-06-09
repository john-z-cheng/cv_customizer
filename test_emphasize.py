import unittest
import write_cv_resume

class TestEmphasisAnyKeywords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        words = ['abc','def','ghi','jkl','mno','pqr','stu','vwxyz']
        cls.line = " ".join(words)
        print(cls.line)

    def test_emphasize_first_word(self):
        keywords = [('abc',[])]
        res = write_cv_resume.emphasize_any_keywords(self.line,keywords)
        self.assertEqual("<b>abc</b> def ghi jkl mno pqr stu vwxyz", res)

    def test_emphasize_middle_word(self):
        """test that one keyword that is in middle of a line is emphasized
        with the HTML elements <b> and </b>"""
        keywords = [('ghi',[])]
        res = write_cv_resume.emphasize_any_keywords(self.line,keywords)
        self.assertEqual("abc def <b>ghi</b> jkl mno pqr stu vwxyz", res)

    def test_emphasize_last_word(self):
        keywords = [('vwxyz',[])]
        res = write_cv_resume.emphasize_any_keywords(self.line,keywords)
        self.assertEqual("abc def ghi jkl mno pqr stu <b>vwxyz</b>", res)

    def test_emphasize_two_words(self):
        keywords = [('def',[]),('vwxyz',[])]
        res = write_cv_resume.emphasize_any_keywords(self.line,keywords)
        self.assertEqual("abc <b>def</b> ghi jkl mno pqr stu <b>vwxyz</b>", res)

    def test_emphasize_two_words_reversed(self):
        keywords = [('vwxyz',[]),('def',[])]
        res = write_cv_resume.emphasize_any_keywords(self.line,keywords)
        self.assertEqual("abc <b>def</b> ghi jkl mno pqr stu <b>vwxyz</b>", res)

if __name__ == '__main__':
    unittest.main(verbosity=0)
