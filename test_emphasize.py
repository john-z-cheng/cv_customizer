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

    def get_keywords(self, line):
        """helper function to create the parameter needed for the test input"""
        key_tuple = write_cv_resume.parse_keywords_line(line)
        return [key_tuple]

    def test_exclusion_slash(self):
        slash_line = "something Python/Tkinter another"
        keywords = self.get_keywords('python|python/tkinter')
        res = write_cv_resume.emphasize_any_keywords(slash_line, keywords)
        self.assertEqual("", res)

    def test_exclusion_start(self):
        slash_line = "something AWS SDK (boto3), ruby on rails, AWS Serverless, more words"
        keywords = self.get_keywords('aws|aws sdk|aws serverless')
        res = write_cv_resume.emphasize_any_keywords(slash_line, keywords)
        self.assertEqual("", res)

    def test_emphasize_first_word(self):
        keywords = self.get_keywords('abc')
        res = write_cv_resume.emphasize_any_keywords(self.line,keywords)
        self.assertEqual("<b>abc</b> def ghi jkl mno pqr stu vwxyz", res)

    def test_emphasize_middle_word(self):
        """test that one keyword that is in middle of a line is emphasized
        with the HTML elements <b> and </b>"""
        keywords = self.get_keywords('ghi')
        res = write_cv_resume.emphasize_any_keywords(self.line,keywords)
        self.assertEqual("abc def <b>ghi</b> jkl mno pqr stu vwxyz", res)

    def test_emphasize_last_word(self):
        keywords = self.get_keywords('vwxyz')
        res = write_cv_resume.emphasize_any_keywords(self.line,keywords)
        self.assertEqual("abc def ghi jkl mno pqr stu <b>vwxyz</b>", res)

    def test_emphasize_two_words(self):
        keywords = self.get_keywords('def')
        keywords.extend(self.get_keywords('vwxyz'))
        res = write_cv_resume.emphasize_any_keywords(self.line,keywords)
        self.assertEqual("abc <b>def</b> ghi jkl mno pqr stu <b>vwxyz</b>", res)

    def test_emphasize_two_words_reversed(self):
        keywords = self.get_keywords('vwxyz')
        keywords.extend(self.get_keywords('def'))
        res = write_cv_resume.emphasize_any_keywords(self.line,keywords)
        self.assertEqual("abc <b>def</b> ghi jkl mno pqr stu <b>vwxyz</b>", res)

    def test_slash_in_keyword(self):
        keywords = self.get_keywords('b/net')
        input_line =  ".abc def. g.hi b/net"
        res = write_cv_resume.emphasize_any_keywords(input_line,keywords)
        self.assertEqual(".abc def. g.hi <b>b/net</b>", res)

    def test_period_in_keyword(self):
        # at start of keyword
        keywords = self.get_keywords('.ghi')
        res = write_cv_resume.emphasize_any_keywords(self.period_line,keywords)
        self.assertEqual(".abc def. <b>.ghi</b> jkl. mno", res)
        # in middle of keyword
        keywords = self.get_keywords('g.hi')
        input_line =  ".abc def. g.hi jal. map"
        res = write_cv_resume.emphasize_any_keywords(input_line,keywords)
        self.assertEqual(".abc def. <b>g.hi</b> jal. map", res)
        # in middle of keyword without match
        keywords = self.get_keywords('g.hi')
        input_line =  ".abc def. gAhi jal. map"
        res = write_cv_resume.emphasize_any_keywords(input_line,keywords)
        self.assertEqual("", res)

    def test_plus_sign_in_keyword(self):
        # single plus sign at end
        keywords = self.get_keywords('CompTIA A+')
        input_line = "Certified with CompTIA A+ and AWS"
        res = write_cv_resume.emphasize_any_keywords(input_line,keywords)
        self.assertEqual("Certified with <b>CompTIA A+</b> and AWS", res)
        # double plus sign at end
        keywords = self.get_keywords('C++')
        input_line = "Programming C++ for 5+ years"
        res = write_cv_resume.emphasize_any_keywords(input_line,keywords)
        self.assertEqual("Programming <b>C++</b> for 5+ years", res)
        # double plus sign with exclusion
        keywords = self.get_keywords('C++|C/C++')
        input_line = "Programming Languages: C/C++, Java, Python"
        res = write_cv_resume.emphasize_any_keywords(input_line,keywords)
        self.assertEqual("", res)

if __name__ == '__main__':
    unittest.main(verbosity=0)
