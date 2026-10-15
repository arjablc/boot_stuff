import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(), "<div><p>First paragraph</p><p>Second paragraph</p></div>"
        )

    def test_to_html_no_tag_raises(self):
        child = LeafNode("p", "Text")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_no_children_raises(self):
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], props={"class": "container"})
        self.assertEqual(
            parent.to_html(), '<div class="container"><span>child</span></div>'
        )

    def test_to_html_with_multiple_props(self):
        child = LeafNode("p", "Text")
        parent = ParentNode(
            "div",
            [child],
            props={"class": "container", "id": "main", "data-test": "value"},
        )
        html = parent.to_html()
        self.assertIn("<div", html)
        self.assertIn('class="container"', html)
        self.assertIn('id="main"', html)
        self.assertIn('data-test="value"', html)
        self.assertIn("><p>Text</p></div>", html)

    def test_to_html_nested_parents(self):
        leaf = LeafNode("b", "bold text")
        child_parent = ParentNode("span", [leaf])
        parent = ParentNode("div", [child_parent])
        self.assertEqual(parent.to_html(), "<div><span><b>bold text</b></span></div>")

    def test_to_html_mixed_children(self):
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode("i", "Italic")
        parent_child = ParentNode("span", [leaf1])
        parent = ParentNode("div", [parent_child, leaf2])
        self.assertEqual(
            parent.to_html(), "<div><span><b>Bold</b></span><i>Italic</i></div>"
        )

    def test_to_html_list(self):
        item1 = LeafNode("li", "Item 1")
        item2 = LeafNode("li", "Item 2")
        item3 = LeafNode("li", "Item 3")
        ul = ParentNode("ul", [item1, item2, item3])
        self.assertEqual(
            ul.to_html(), "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
        )

    def test_to_html_paragraph_with_formatting(self):
        bold = LeafNode("b", "bold")
        italic = LeafNode("i", "italic")
        text = LeafNode(None, " and ")
        p = ParentNode("p", [bold, text, italic])
        self.assertEqual(p.to_html(), "<p><b>bold</b> and <i>italic</i></p>")

    def test_to_html_deeply_nested(self):
        deep_leaf = LeafNode("span", "deep")
        level3 = ParentNode("div", [deep_leaf])
        level2 = ParentNode("div", [level3])
        level1 = ParentNode("div", [level2])
        self.assertEqual(
            level1.to_html(), "<div><div><div><span>deep</span></div></div></div>"
        )

    def test_to_html_heading_with_children(self):
        bold = LeafNode("b", "Important")
        text = LeafNode(None, " Title")
        h1 = ParentNode("h1", [bold, text])
        self.assertEqual(h1.to_html(), "<h1><b>Important</b> Title</h1>")

    def test_to_html_complex_structure(self):
        # <div class="wrapper">
        #   <h1>Title</h1>
        #   <p>Text with <b>bold</b> word</p>
        # </div>
        h1 = LeafNode("h1", "Title")
        bold = LeafNode("b", "bold")
        text1 = LeafNode(None, "Text with ")
        text2 = LeafNode(None, " word")
        p = ParentNode("p", [text1, bold, text2])
        div = ParentNode("div", [h1, p], props={"class": "wrapper"})
        self.assertEqual(
            div.to_html(),
            '<div class="wrapper"><h1>Title</h1><p>Text with <b>bold</b> word</p></div>',
        )


if __name__ == "__main__":
    unittest.main()
