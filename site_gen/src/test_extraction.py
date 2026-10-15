import unittest


from md_extrators import extract_title


class TestExtraction(unittest.TestCase):
    def test_h1_whitespaces(self):
        markdown = "    # Title"
        e_res = "Title"
        res = extract_title(markdown)
        self.assertEqual(e_res, res)

    def test_h1_no_h1(self):
        markdown = "     Title"
        self.assertRaises(Exception, extract_title, markdown)
