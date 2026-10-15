import unittest


from conversion_pipeline import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph_with_inline_markdown(self):
        node = markdown_to_html_node("This is **bold** and _italic_")

        self.assertEqual(
            node.to_html(), "<div><p>This is <b>bold</b> and <i>italic</i></p></div>"
        )

    def test_heading_with_inline_markdown(self):
        node = markdown_to_html_node("## Hello **world**")

        self.assertEqual(node.to_html(), "<div><h2>Hello <b>world</b></h2></div>")

    def test_code_block(self):
        node = markdown_to_html_node("```\nprint('hello')\n```")

        self.assertEqual(
            node.to_html(), "<div><pre><code>print('hello')\n</code></pre></div>"
        )

    def test_quote_block(self):
        node = markdown_to_html_node("> quoted\n> text with `code`")

        self.assertEqual(
            node.to_html(),
            "<div><blockquote>quoted text with <code>code</code></blockquote></div>",
        )

    def test_quote_block_with_bold_text(self):
        node = markdown_to_html_node("> quote with **bold** text")

        self.assertEqual(
            node.to_html(),
            "<div><blockquote>quote with <b>bold</b> text</blockquote></div>",
        )

    def test_unordered_list(self):
        node = markdown_to_html_node("- first\n- second")

        self.assertEqual(
            node.to_html(),
            "<div><ul><li>first</li><li>second</li></ul></div>",
        )

    def test_unordered_list_with_inline_markdown(self):
        node = markdown_to_html_node(
            "- **first**\n- second with [link](https://example.com)"
        )

        self.assertEqual(
            node.to_html(),
            '<div><ul><li><b>first</b></li><li>second with <a href="https://example.com">link</a></li></ul></div>',
        )

    def test_ordered_list(self):
        node = markdown_to_html_node("1. first\n2. second")

        self.assertEqual(
            node.to_html(),
            "<div><ol><li>first</li><li>second</li></ol></div>",
        )

    def test_ordered_list_with_inline_markdown(self):
        node = markdown_to_html_node("1. first with _italic_\n2. second with `code`")

        self.assertEqual(
            node.to_html(),
            "<div><ol><li>first with <i>italic</i></li><li>second with <code>code</code></li></ol></div>",
        )

    def test_paragraph_single_newline_becomes_space(self):
        node = markdown_to_html_node("first line\nsecond line")

        self.assertEqual(node.to_html(), "<div><p>first line second line</p></div>")

    def test_heading_level_four(self):
        node = markdown_to_html_node("#### Tiny heading")

        self.assertEqual(node.to_html(), "<div><h4>Tiny heading</h4></div>")

    def test_multiple_mixed_blocks(self):
        markdown = "# Title\n\n> quoted\n> line\n\n1. first\n2. second\n\n```\ncode sample\n```"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><blockquote>quoted line</blockquote><ol><li>first</li><li>second</li></ol><pre><code>code sample\n</code></pre></div>",
        )

    def test_multiple_blocks(self):
        markdown = "# Title\n\nParagraph with [link](https://example.com)\n\n- item one\n- item two"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            '<div><h1>Title</h1><p>Paragraph with <a href="https://example.com">link</a></p><ul><li>item one</li><li>item two</li></ul></div>',
        )


if __name__ == "__main__":
    unittest.main()
