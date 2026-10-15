import unittest
from textnode import TextNode, TextType
from converters import text_node_to_html_node


class TestConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_link_with_boot_dev(self):
        node = TextNode(
            "This is some anchor text", TextType.LINK, "https://www.boot.dev"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is some anchor text")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image(self):
        node = TextNode(
            "Image description", TextType.IMAGE_LINK, "https://example.com/image.jpg"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/image.jpg", "alt": "Image description"},
        )

    def test_text_to_html(self):
        node = TextNode("Plain text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "Plain text")

    def test_bold_to_html(self):
        node = TextNode("Bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Bold</b>")

    def test_italic_to_html(self):
        node = TextNode("Italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>Italic</i>")

    def test_code_to_html(self):
        node = TextNode("x = 5", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>x = 5</code>")

    def test_link_to_html(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(), '<a href="https://example.com">Link text</a>'
        )

    # def test_image_to_html(self):
    #     node = TextNode("Alt text", TextType.IMAGE_LINK, "https://example.com/pic.png")
    #     html_node = text_node_to_html_node(node)
    #     print(html_node)
    #     html = html_node.to_html()
    #     # Note: This will raise ValueError because img has empty value
    #     # You may need to adjust your LeafNode implementation for self-closing tags
    #     print(html)
    #
    # def test_unsupported_type_raises(self):
    #     # If you have other enum values not handled
    #     # This test assumes there's a way to create an invalid type
    #     # You might need to adjust based on your TextType enum
    #     pass  # Skip if all types are handled

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")

    def test_empty_bold(self):
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, "b")
