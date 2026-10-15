import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from md_extrators import extract_markdown_images, extract_markdown_urls


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        """Test extracting a single image"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        result = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        """Test extracting multiple images"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(result, expected)

    def test_no_images(self):
        """Test with text containing no images"""
        text = "This is just plain text with no images"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_images_with_links(self):
        """Test that regular links are not extracted as images"""
        text = "This has a [link](https://example.com) and ![image](https://img.com/pic.png)"
        result = extract_markdown_images(text)
        expected = [("image", "https://img.com/pic.png")]
        self.assertEqual(result, expected)

    def test_empty_alt_text(self):
        """Test image with empty alt text"""
        text = "Image with no alt ![](https://example.com/img.png)"
        result = extract_markdown_images(text)
        expected = [("", "https://example.com/img.png")]
        self.assertEqual(result, expected)

    def test_empty_url(self):
        """Test image with empty URL"""
        text = "Image with no URL ![alt text]()"
        result = extract_markdown_images(text)
        expected = [("alt text", "")]
        self.assertEqual(result, expected)

    def test_image_at_start(self):
        """Test image at the start of text"""
        text = "![first](https://example.com/first.png) followed by text"
        result = extract_markdown_images(text)
        expected = [("first", "https://example.com/first.png")]
        self.assertEqual(result, expected)

    def test_image_at_end(self):
        """Test image at the end of text"""
        text = "Text followed by ![last](https://example.com/last.png)"
        result = extract_markdown_images(text)
        expected = [("last", "https://example.com/last.png")]
        self.assertEqual(result, expected)

    def test_consecutive_images(self):
        """Test consecutive images with no text between"""
        text = "![first](https://example.com/1.png)![second](https://example.com/2.png)"
        result = extract_markdown_images(text)
        expected = [
            ("first", "https://example.com/1.png"),
            ("second", "https://example.com/2.png"),
        ]
        self.assertEqual(result, expected)

    def test_image_with_special_chars_in_alt(self):
        """Test image with special characters in alt text"""
        text = "![alt with spaces & symbols!](https://example.com/img.png)"
        result = extract_markdown_images(text)
        expected = [("alt with spaces & symbols!", "https://example.com/img.png")]
        self.assertEqual(result, expected)

    def test_nested_brackets_not_matched(self):
        """Test that nested brackets are not matched"""
        text = "![[nested]](https://example.com/img.png)"
        result = extract_markdown_images(text)
        # Regex should not match nested brackets
        self.assertEqual(result, [])

    def test_nested_parentheses_not_matched(self):
        """Test that nested parentheses are not matched"""
        text = "![alt](https://example.com/(nested).png)"
        result = extract_markdown_images(text)
        # Regex should not match nested parentheses
        self.assertEqual(result, [])


class TestExtractMarkdownUrls(unittest.TestCase):
    def test_single_url(self):
        """Test extracting a single URL"""
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        result = extract_markdown_urls(text)
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(result, expected)

    def test_multiple_urls(self):
        """Test extracting multiple URLs"""
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_urls(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(result, expected)

    def test_no_urls(self):
        """Test with text containing no URLs"""
        text = "This is just plain text with no links"
        result = extract_markdown_urls(text)
        self.assertEqual(result, [])

    def test_urls_with_images(self):
        """Test that images are not extracted as URLs"""
        text = "This has a ![image](https://img.com/pic.png) and [link](https://example.com)"
        result = extract_markdown_urls(text)
        expected = [("link", "https://example.com")]
        self.assertEqual(result, expected)

    def test_empty_link_text(self):
        """Test URL with empty link text"""
        text = "Link with no text [](https://example.com)"
        result = extract_markdown_urls(text)
        expected = [("", "https://example.com")]
        self.assertEqual(result, expected)

    def test_empty_url(self):
        """Test URL with empty href"""
        text = "Link with no URL [link text]()"
        result = extract_markdown_urls(text)
        expected = [("link text", "")]
        self.assertEqual(result, expected)

    def test_url_at_start(self):
        """Test URL at the start of text"""
        text = "[first](https://example.com) followed by text"
        result = extract_markdown_urls(text)
        expected = [("first", "https://example.com")]
        self.assertEqual(result, expected)

    def test_url_at_end(self):
        """Test URL at the end of text"""
        text = "Text followed by [last](https://example.com)"
        result = extract_markdown_urls(text)
        expected = [("last", "https://example.com")]
        self.assertEqual(result, expected)

    def test_consecutive_urls(self):
        """Test consecutive URLs with no text between"""
        text = "[first](https://example.com/1)[second](https://example.com/2)"
        result = extract_markdown_urls(text)
        expected = [
            ("first", "https://example.com/1"),
            ("second", "https://example.com/2"),
        ]
        self.assertEqual(result, expected)

    def test_url_with_special_chars_in_text(self):
        """Test URL with special characters in link text"""
        text = "[link with spaces & symbols!](https://example.com)"
        result = extract_markdown_urls(text)
        expected = [("link with spaces & symbols!", "https://example.com")]
        self.assertEqual(result, expected)

    def test_mixed_images_and_urls(self):
        """Test text with both images and URLs"""
        text = "A [link](https://example.com) and ![image](https://img.com/pic.png) together"
        result = extract_markdown_urls(text)
        expected = [("link", "https://example.com")]
        self.assertEqual(result, expected)

    def test_image_before_url(self):
        """Test that image immediately before URL doesn't interfere"""
        text = "![img](https://img.com/pic.png)[link](https://example.com)"
        result = extract_markdown_urls(text)
        expected = [("link", "https://example.com")]
        self.assertEqual(result, expected)

    def test_nested_brackets_not_matched(self):
        """Test that nested brackets are not matched"""
        text = "[[nested]](https://example.com)"
        result = extract_markdown_urls(text)
        # Regex should not match nested brackets
        self.assertEqual(result, [])

    def test_nested_parentheses_not_matched(self):
        """Test that nested parentheses are not matched"""
        text = "[link](https://example.com/(nested))"
        result = extract_markdown_urls(text)
        # Regex should not match nested parentheses
        self.assertEqual(result, [])

    def test_url_with_query_params(self):
        """Test URL with query parameters"""
        text = "[search](https://google.com/search?q=test&lang=en)"
        result = extract_markdown_urls(text)
        expected = [("search", "https://google.com/search?q=test&lang=en")]
        self.assertEqual(result, expected)

    def test_url_with_fragment(self):
        """Test URL with fragment identifier"""
        text = "[section](https://example.com/page#section)"
        result = extract_markdown_urls(text)
        expected = [("section", "https://example.com/page#section")]
        self.assertEqual(result, expected)


class TestBothFunctionsTogether(unittest.TestCase):
    """Test both functions with the same text to ensure they don't interfere"""

    def test_combined_text_images(self):
        """Test extracting images from combined text"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and a link [to boot dev](https://www.boot.dev)"
        result = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(result, expected)

    def test_combined_text_urls(self):
        """Test extracting URLs from combined text"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_urls(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
