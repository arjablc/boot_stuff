import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", props={"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_to_html_empty_value_raises(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_none_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Container content")
        self.assertEqual(node.to_html(), "<div>Container content</div>")

    def test_leaf_to_html_span_with_props(self):
        node = LeafNode(
            "span", "Styled text", props={"class": "highlight", "id": "main"}
        )
        self.assertEqual(
            node.to_html(), '<span class="highlight" id="main">Styled text</span>'
        )

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Title")
        self.assertEqual(node.to_html(), "<h1>Title</h1>")

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", props={"src": "image.jpg", "alt": "Description"})
        # Note: This will raise ValueError due to empty value
        # If you want img tags to work, you'd need to adjust the implementation
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "print('hello')")
        self.assertEqual(node.to_html(), "<code>print('hello')</code>")

    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_italic(self):
        node = LeafNode("i", "Italic text")
        self.assertEqual(node.to_html(), "<i>Italic text</i>")

    def test_leaf_repr(self):
        node = LeafNode("a", "Link", props={"href": "https://example.com"})
        repr_str = repr(node)
        self.assertIn("LeafNode", repr_str)
        self.assertIn("a", repr_str)
        self.assertIn("Link", repr_str)
        self.assertIn("href", repr_str)

    def test_leaf_repr_no_props(self):
        node = LeafNode("p", "Text")
        repr_str = repr(node)
        self.assertIn("LeafNode", repr_str)
        self.assertIn("p", repr_str)
        self.assertIn("Text", repr_str)

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode(
            "a",
            "Click here",
            props={"href": "https://example.com", "target": "_blank", "class": "link"},
        )
        html = node.to_html()
        self.assertIn("<a", html)
        self.assertIn('href="https://example.com"', html)
        self.assertIn('target="_blank"', html)
        self.assertIn('class="link"', html)
        self.assertIn(">Click here</a>", html)


if __name__ == "__main__":
    unittest.main()
