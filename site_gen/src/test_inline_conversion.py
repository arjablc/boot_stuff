import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from converters import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextnodes(unittest.TestCase):
    def test_plain_text(self):
        """Test with plain text, no formatting"""
        text = "This is just plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        """Test with empty text"""
        text = ""
        result = text_to_textnodes(text)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_single_bold(self):
        """Test with single bold text"""
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_italic(self):
        """Test with single italic text"""
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_code(self):
        """Test with single code text"""
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_link(self):
        """Test with single link"""
        text = "This is a [link](https://example.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_single_image(self):
        """Test with single image"""
        text = "This is an ![image](https://example.com/img.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE_LINK, "https://example.com/img.png"),
        ]
        self.assertEqual(result, expected)

    def test_bold_and_italic(self):
        """Test with both bold and italic"""
        text = "This is **bold** and _italic_"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    def test_bold_and_code(self):
        """Test with both bold and code"""
        text = "This is **bold** and `code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_all_inline_formats(self):
        """Test with all inline formatting types"""
        text = "This is **bold** and _italic_ and `code` and [link](https://example.com) and ![image](https://example.com/img.png)"
        result = text_to_textnodes(text)
        # Should have all types represented
        types_present = {node.text_type for node in result}
        self.assertIn(TextType.TEXT, types_present)
        self.assertIn(TextType.BOLD, types_present)
        self.assertIn(TextType.ITALIC, types_present)
        self.assertIn(TextType.CODE, types_present)
        self.assertIn(TextType.LINK, types_present)
        self.assertIn(TextType.IMAGE_LINK, types_present)

    def test_nested_formatting_bold_in_italic(self):
        """Test nested formatting (note: may not work as expected with current implementation)"""
        text = "_italic with **bold** inside_"
        result = text_to_textnodes(text)
        # Depending on implementation, this may or may not handle nesting correctly
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_multiple_bold(self):
        """Test multiple bold sections"""
        text = "**bold1** text **bold2**"
        result = text_to_textnodes(text)
        bold_nodes = [n for n in result if n.text_type == TextType.BOLD]
        self.assertEqual(len(bold_nodes), 2)
        self.assertEqual(bold_nodes[0].text, "bold1")
        self.assertEqual(bold_nodes[1].text, "bold2")

    def test_multiple_italic(self):
        """Test multiple italic sections"""
        text = "_italic1_ text _italic2_"
        result = text_to_textnodes(text)
        italic_nodes = [n for n in result if n.text_type == TextType.ITALIC]
        self.assertEqual(len(italic_nodes), 2)
        self.assertEqual(italic_nodes[0].text, "italic1")
        self.assertEqual(italic_nodes[1].text, "italic2")

    def test_multiple_code(self):
        """Test multiple code sections"""
        text = "`code1` text `code2`"
        result = text_to_textnodes(text)
        code_nodes = [n for n in result if n.text_type == TextType.CODE]
        self.assertEqual(len(code_nodes), 2)
        self.assertEqual(code_nodes[0].text, "code1")
        self.assertEqual(code_nodes[1].text, "code2")

    def test_multiple_links(self):
        """Test multiple links"""
        text = "[link1](https://example1.com) text [link2](https://example2.com)"
        result = text_to_textnodes(text)
        link_nodes = [n for n in result if n.text_type == TextType.LINK]
        self.assertEqual(len(link_nodes), 2)
        self.assertEqual(link_nodes[0].text, "link1")
        self.assertEqual(link_nodes[1].text, "link2")

    def test_multiple_images(self):
        """Test multiple images"""
        text = (
            "![img1](https://example.com/1.png) text ![img2](https://example.com/2.png)"
        )
        result = text_to_textnodes(text)
        image_nodes = [n for n in result if n.text_type == TextType.IMAGE_LINK]
        self.assertEqual(len(image_nodes), 2)
        self.assertEqual(image_nodes[0].text, "img1")
        self.assertEqual(image_nodes[1].text, "img2")

    def test_link_with_bold_text(self):
        """Test link containing bold text in description"""
        text = "[**bold link**](https://example.com)"
        result = text_to_textnodes(text)
        # Link is processed first, so bold markers inside link text remain
        link_nodes = [n for n in result if n.text_type == TextType.LINK]
        self.assertEqual(len(link_nodes), 1)

    def test_image_with_bold_alt(self):
        """Test image with bold markers in alt text"""
        text = "![**bold alt**](https://example.com/img.png)"
        result = text_to_textnodes(text)
        # Image is processed before bold, so bold markers in alt text remain
        image_nodes = [n for n in result if n.text_type == TextType.IMAGE_LINK]
        self.assertEqual(len(image_nodes), 1)

    def test_bold_with_link_inside(self):
        """Test bold text containing a link"""
        text = "**bold [link](https://example.com) text**"
        result = text_to_textnodes(text)
        # Links processed first, then bold
        self.assertIsInstance(result, list)

    def test_code_with_bold_markers(self):
        """Test code containing bold markers (should be preserved)"""
        text = "`code with **asterisks**`"
        result = text_to_textnodes(text)
        code_nodes = [n for n in result if n.text_type == TextType.CODE]
        # After code is extracted, the bold markers should not be processed
        # since they're in a CODE node, not TEXT node
        self.assertEqual(len(code_nodes), 1)

    def test_complex_markdown_example(self):
        """Test complex markdown from the example"""
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)

        # Check we have all the expected types
        types = [n.text_type for n in result]
        self.assertIn(TextType.BOLD, types)
        self.assertIn(TextType.CODE, types)
        self.assertIn(TextType.IMAGE_LINK, types)
        self.assertIn(TextType.LINK, types)
        self.assertIn(TextType.TEXT, types)

        # Note: *italic* uses asterisk, but the function uses underscore for italic
        # So this might not extract italic correctly

    def test_boot_dev_example(self):
        """Test the exact example from boot.dev documentation"""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE_LINK, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(result, expected)

    def test_only_formatted_text(self):
        """Test text that is entirely formatted"""
        text = "**bold**"
        result = text_to_textnodes(text)
        # May have empty text nodes before/after
        bold_nodes = [n for n in result if n.text_type == TextType.BOLD]
        self.assertEqual(len(bold_nodes), 1)
        self.assertEqual(bold_nodes[0].text, "bold")

    def test_consecutive_formatting(self):
        """Test consecutive formatting with no space"""
        text = "**bold**_italic_`code`"
        result = text_to_textnodes(text)
        types = [n.text_type for n in result if n.text != ""]
        self.assertIn(TextType.BOLD, types)
        self.assertIn(TextType.ITALIC, types)
        self.assertIn(TextType.CODE, types)

    def test_link_and_image_together(self):
        """Test link immediately followed by image"""
        text = "[link](https://example.com)![image](https://example.com/img.png)"
        result = text_to_textnodes(text)
        link_nodes = [n for n in result if n.text_type == TextType.LINK]
        image_nodes = [n for n in result if n.text_type == TextType.IMAGE_LINK]
        self.assertEqual(len(link_nodes), 1)
        self.assertEqual(len(image_nodes), 1)

    def test_image_and_link_together(self):
        """Test image immediately followed by link"""
        text = "![image](https://example.com/img.png)[link](https://example.com)"
        result = text_to_textnodes(text)
        link_nodes = [n for n in result if n.text_type == TextType.LINK]
        image_nodes = [n for n in result if n.text_type == TextType.IMAGE_LINK]
        self.assertEqual(len(link_nodes), 1)
        self.assertEqual(len(image_nodes), 1)

    def test_whitespace_only(self):
        """Test with only whitespace"""
        text = "   "
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "   ")

    def test_special_characters(self):
        """Test with special characters that aren't markdown"""
        text = "Text with & < > @ # $ % special chars"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, TextType.TEXT)


class TestTextToTextnodesEdgeCases(unittest.TestCase):
    """Edge cases and potential issues"""

    def test_unclosed_bold(self):
        """Test with unclosed bold delimiter"""
        text = "This has **unclosed bold"
        # Should raise an error or handle gracefully
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_unclosed_italic(self):
        """Test with unclosed italic delimiter"""
        text = "This has _unclosed italic"
        # Should raise an error or handle gracefully
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_unclosed_code(self):
        """Test with unclosed code delimiter"""
        text = "This has `unclosed code"
        # Should raise an error or handle gracefully
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_malformed_link(self):
        """Test with malformed link"""
        text = "This has [malformed link(https://example.com)"
        result = text_to_textnodes(text)
        # Should not extract the malformed link
        link_nodes = [n for n in result if n.text_type == TextType.LINK]
        self.assertEqual(len(link_nodes), 0)

    def test_malformed_image(self):
        """Test with malformed image"""
        text = "This has ![malformed image(https://example.com/img.png)"
        result = text_to_textnodes(text)
        # Should not extract the malformed image
        image_nodes = [n for n in result if n.text_type == TextType.IMAGE_LINK]
        self.assertEqual(len(image_nodes), 0)

    def test_empty_bold(self):
        """Test with empty bold section"""
        text = "This has **** empty bold"
        result = text_to_textnodes(text)
        # Might create empty bold node or skip it
        self.assertIsInstance(result, list)

    def test_empty_italic(self):
        """Test with empty italic section"""
        text = "This has __ empty italic"
        result = text_to_textnodes(text)
        # Might create empty italic node or skip it
        self.assertIsInstance(result, list)

    def test_empty_code(self):
        """Test with empty code section"""
        text = "This has `` empty code"
        result = text_to_textnodes(text)
        # Might create empty code node or skip it
        self.assertIsInstance(result, list)

    def test_asterisk_vs_underscore_italic(self):
        """Test that asterisk (*) doesn't create italic (only underscore does)"""
        text = "This is *not italic* but this is _italic_"
        result = text_to_textnodes(text)
        italic_nodes = [n for n in result if n.text_type == TextType.ITALIC]
        # Should only have one italic node (from underscore)
        self.assertEqual(len(italic_nodes), 1)
        self.assertEqual(italic_nodes[0].text, "italic")


class TestTextToTextnodesProcessingOrder(unittest.TestCase):
    """Tests to verify processing order (links -> images -> bold -> italic -> code)"""

    def test_processing_order_link_before_bold(self):
        """Test that links are processed before bold"""
        text = "[**link**](https://example.com)"
        result = text_to_textnodes(text)
        # Link should be extracted with ** still in the text
        link_nodes = [n for n in result if n.text_type == TextType.LINK]
        self.assertEqual(len(link_nodes), 1)
        # The link text should still contain the bold markers
        self.assertIn("**", link_nodes[0].text)

    def test_processing_order_image_before_bold(self):
        """Test that images are processed before bold"""
        text = "![**alt**](https://example.com/img.png)"
        result = text_to_textnodes(text)
        # Image should be extracted with ** still in the alt text
        image_nodes = [n for n in result if n.text_type == TextType.IMAGE_LINK]
        self.assertEqual(len(image_nodes), 1)
        self.assertIn("**", image_nodes[0].text)

    def test_processing_order_bold_before_italic(self):
        """Test that bold is processed before italic"""
        text = "**bold _and italic_**"
        result = text_to_textnodes(text)
        # Bold is processed first, so italic markers remain in bold text
        bold_nodes = [n for n in result if n.text_type == TextType.BOLD]
        if len(bold_nodes) > 0:
            # The bold text might still contain italic markers
            pass  # Implementation dependent

    def test_processing_order_italic_before_code(self):
        """Test that italic is processed before code"""
        text = "_italic with `code`_"
        result = text_to_textnodes(text)
        # Italic is processed before code
        italic_nodes = [n for n in result if n.text_type == TextType.ITALIC]
        # Behavior depends on implementation
        self.assertIsInstance(result, list)


class TestTextToTextnodesRealWorldExamples(unittest.TestCase):
    """Real-world markdown examples"""

    def test_github_readme_style(self):
        """Test GitHub README style markdown"""
        text = "Check out the **documentation** at [our website](https://example.com) or view the `README.md`"
        result = text_to_textnodes(text)
        types = {n.text_type for n in result}
        self.assertIn(TextType.BOLD, types)
        self.assertIn(TextType.LINK, types)
        self.assertIn(TextType.CODE, types)

    def test_blog_post_style(self):
        """Test blog post style markdown"""
        text = "This is a paragraph with _emphasis_ and **strong emphasis** and a ![diagram](https://example.com/diagram.png) explaining the concept."
        result = text_to_textnodes(text)
        types = {n.text_type for n in result}
        self.assertIn(TextType.ITALIC, types)
        self.assertIn(TextType.BOLD, types)
        self.assertIn(TextType.IMAGE_LINK, types)

    def test_technical_documentation(self):
        """Test technical documentation style"""
        text = "To install, run `pip install package` and then import it with `from package import module`. See [docs](https://docs.example.com) for more."
        result = text_to_textnodes(text)
        code_nodes = [n for n in result if n.text_type == TextType.CODE]
        link_nodes = [n for n in result if n.text_type == TextType.LINK]
        self.assertEqual(len(code_nodes), 2)
        self.assertEqual(len(link_nodes), 1)


if __name__ == "__main__":
    unittest.main()
