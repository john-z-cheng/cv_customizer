import unittest
import write_cv_resume

class TestEmphasisAnyKeywords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        words = ['abc','def','ghi','jkl','mno','pqr','stu','vwxyz']
        period_words = ['.abc','def.','.ghi','jkl.','mno']
        cls.line = " ".join(words)
        cls.period_line = " ".join(period_words)
        print(cls.line)
        print(cls.period_line)

    def test_exclusion_slash(self):
        slash_line = "something Python/Tkinter another"
        keywords = [('python',["python/tkinter"])]
        res = write_cv_resume.emphasize_any_keywords(slash_line, keywords)
        self.assertEqual("", res)

    def test_exclusion_start(self):
        slash_line = "something AWS SDK (boto3), ruby on rails, AWS Serverless, more words"
        keywords = [('aws',["aws sdk","aws serverless"])]
        res = write_cv_resume.emphasize_any_keywords(slash_line, keywords)
        self.assertEqual("", res)

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

    def test_period_start_word(self):
        keywords = [('.ghi',[])]
        res = write_cv_resume.emphasize_any_keywords(self.period_line,keywords)
        self.assertEqual(".abc def. <b>.ghi</b> jkl. mno", res)

    def test_period_middle_word(self):
        keywords = [('g.hi',[])]
        input_line =  ".abc def. g.hi jal. map"
        res = write_cv_resume.emphasize_any_keywords(input_line,keywords)
        self.assertEqual(".abc def. <b>g.hi</b> jal. map", res)

    def test_period_middle_word_no_match(self):
        """Tests that the period in keyword is not treated as any character in regex so
        there should not be a match and the returned result is empty string"""
        keywords = [('g.hi',[])]
        input_line =  ".abc def. gAhi jal. map"
        res = write_cv_resume.emphasize_any_keywords(input_line,keywords)
        self.assertEqual("", res)


if __name__ == '__main__':
    unittest.main(verbosity=0)
