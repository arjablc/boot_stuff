import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "h1",
            "Title",
            props={"href": "https://google.com", "target": "_blank"},
        )
        html = ' href="https://google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), html)

    def test_props_to_html_single_prop(self):
        node = HTMLNode("a", "Link", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "Text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        node = HTMLNode("div", "Content", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_tag_assignment(self):
        node = HTMLNode("div", "Content")
        self.assertEqual(node.tag, "div")

    def test_value_assignment(self):
        node = HTMLNode("p", "Hello World")
        self.assertEqual(node.value, "Hello World")

    def test_children_assignment(self):
        child1 = HTMLNode("span", "Child 1")
        child2 = HTMLNode("span", "Child 2")
        parent = HTMLNode("div", None, children=[child1, child2])
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].value, "Child 1")
        self.assertEqual(parent.children[1].value, "Child 2")

    def test_no_children(self):
        node = HTMLNode("p", "Text")
        self.assertIsNone(node.children)

    def test_no_tag(self):
        node = HTMLNode(None, "Just text")
        self.assertIsNone(node.tag)

    def test_no_value(self):
        node = HTMLNode("div", None)
        self.assertIsNone(node.value)

    def test_repr(self):
        node = HTMLNode("a", "Link", props={"href": "https://example.com"})
        repr_str = repr(node)
        self.assertIn("a", repr_str)
        self.assertIn("Link", repr_str)
        self.assertIn("href", repr_str)

    def test_all_parameters(self):
        child = HTMLNode("span", "Child")
        node = HTMLNode(
            tag="div",
            value="Parent",
            children=[child],
            props={"class": "container", "id": "main"},
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Parent")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.props["class"], "container")
