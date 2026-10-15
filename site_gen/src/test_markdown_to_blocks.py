import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from converters import BlockType, block_to_block_type, markdown_to_blocks


class TestBlockConversions(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_ignores_extra_empty_blocks(self):
        md = "\n\nFirst block\n\n\n\nSecond block\n\n\n"
        blocks = markdown_to_blocks(md)

        self.assertEqual(blocks, ["First block", "Second block"])

    def test_markdown_to_blocks_returns_empty_list_for_whitespace_only_input(self):
        md = "\n\n   \n\t\n\n"
        blocks = markdown_to_blocks(md)

        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_trims_surrounding_whitespace_per_block(self):
        md = "  First block with spaces   \n\n\tSecond block with tabs\t\n\n  Third block  "
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "First block with spaces",
                "Second block with tabs",
                "Third block",
            ],
        )

    def test_markdown_to_blocks_keeps_single_newlines_inside_block(self):
        md = "First line\nSecond line\nThird line"
        blocks = markdown_to_blocks(md)

        self.assertEqual(blocks, ["First line\nSecond line\nThird line"])

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
