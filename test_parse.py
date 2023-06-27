import unittest
import write_cv_resume

class TestParseKeywordsLine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def get_keywords(self, line):
        """helper function to create the parameter needed for the test input"""
        key_tuple = write_cv_resume.parse_keywords_line(line)
        return [key_tuple]

    def test_comment_lines(self):
        line1 = "// This is a comment line to be ignored"
        line2 = "-- Comment with double dash --"
        line3 = "keyword phrase"
        line4 = "  -- comment that has whitespace at beginning"
        key_tuple = write_cv_resume.parse_keywords_line(line1)
        self.assertEqual(None, key_tuple)
        key_tuple = write_cv_resume.parse_keywords_line(line2)
        self.assertEqual(None, key_tuple)
        key_tuple = write_cv_resume.parse_keywords_line(line3)
        self.assertNotEqual(None, key_tuple)
        key_tuple = write_cv_resume.parse_keywords_line(line4)
        self.assertEqual(None, key_tuple)

if __name__ == '__main__':
    unittest.main(verbosity=0)
