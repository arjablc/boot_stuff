import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://hello.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_test_type(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://hello.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://hello.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
