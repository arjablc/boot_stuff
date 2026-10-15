import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from textnode import TextNode, TextType
from converters import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_empty_list(self):
        """Test with empty list of nodes"""
        result = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertIsNone(result)

    def test_node_without_delimiter(self):
        """Test with node that doesn't contain the delimiter"""
        node = TextNode("plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertIsInstance(result, list)

    def test_single_bold_section(self):
        """Test splitting a single bold section"""
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_bold_sections(self):
        """Test splitting multiple bold sections"""
        node = TextNode("**bold1** and **bold2**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_code_delimiter(self):
        """Test with code delimiter (backticks)"""
        node = TextNode("This is `code` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    #
    def test_italic_delimiter(self):
        """Test with italic delimiter"""
        node = TextNode("This is *italic* text", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    #
    def test_non_text_node_preserved(self):
        """Test that non-TEXT nodes are preserved unchanged"""
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("normal **bold**", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result[0], TextNode("already bold", TextType.BOLD))

    #
    def test_multiple_nodes_mixed(self):
        """Test with multiple nodes of different types"""
        nodes = [
            TextNode("First **bold**", TextType.TEXT),
            TextNode("already italic", TextType.ITALIC),
            TextNode("Second **bold**", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertIsInstance(result, list)
        self.assertIn(TextNode("already italic", TextType.ITALIC), result)

    def test_unclosed_delimiter(self):
        """Test with unclosed delimiter (should raise error or handle gracefully)"""
        node = TextNode("This has **unclosed bold", TextType.TEXT)
        # This should ideally raise an error or handle gracefully
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delimiter_at_start(self):
        """Test with delimiter at the start"""
        node = TextNode("**bold** at start", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    #
    def test_delimiter_at_end(self):
        """Test with delimiter at the end"""
        node = TextNode("at end **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("at end ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
