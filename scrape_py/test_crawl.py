import unittest

from crawl import (
    extract_page_data,
    get_first_paragraph_from_html,
    get_heading_from_html,
    get_images_from_html,
    get_urls_from_html,
    normalize_url,
)


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)


class TestHeadingExtract(unittest.TestCase):
    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2(self):
        input_body = "<html><body><h2>Test Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_no_heading(self):
        input_body = "<html><body>Test Title</body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)


class TestPExtract(unittest.TestCase):
    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <p>Main paragraph.</p>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_ptag(self):
        input_body = """<html><body>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)


class TestUrls(unittest.TestCase):
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = (
            '<html><body><a href="/dev/main"><span>Boot.dev</span></a></body></html>'
        )
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/dev/main"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_none(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body>https://this_is_link_to_something.com/</body></html>"
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)


class TestImages(unittest.TestCase):
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://example.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://example.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_none(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body></body></html>"
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)


class TestPageData(unittest.TestCase):
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_missing_elements(self):
        # Tests behavior when expected tags (h1, p) are completely missing,
        # and when anchor/image tags exist but lack href/src attributes.
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
                <div>No heading or paragraph here.</div>
                <a name="section1">Anchor without href</a>
                <img alt="Image without src">
            </body></html>"""

        actual = extract_page_data(input_body, input_url)

        expected = {
            "url": "https://crawler-test.com",
            "heading": "",  # or "", depending on your implementation
            "first_paragraph": "",  # or "", depending on your implementation
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_absolute_urls(self):
        # Tests that the extraction correctly handles URLs that are already absolute
        # and doesn't incorrectly append the base_url to them.
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>External Links</h1>
            <p>Testing absolute paths.</p>
            <a href="https://external-site.com/about">External Link</a>
            <img src="http://cdn.images.com/logo.png" alt="External Image">
        </body></html>"""

        actual = extract_page_data(input_body, input_url)

        expected = {
            "url": "https://crawler-test.com",
            "heading": "External Links",
            "first_paragraph": "Testing absolute paths.",
            "outgoing_links": ["https://external-site.com/about"],
            "image_urls": ["http://cdn.images.com/logo.png"],
        }
        self.assertEqual(actual, expected)

        def test_extract_page_data_multiple_elements(self):
            # Tests that only the FIRST heading and paragraph are extracted,
            # while ALL valid links and images are collected into the lists.
            input_url = "https://crawler-test.com"
            input_body = """<html><body>
                <h1>First Title</h1>
                <h1>Second Title (Should be ignored)</h1>
                <p>This is the first paragraph.</p>
                <p>This is the second paragraph.</p>
                <a href="/link1">Link 1</a>
                <a href="/link2">Link 2</a>
                <img src="/image1.jpg" alt="Image 1">
                <img src="/image2.jpg" alt="Image 2">
            </body></html>"""

            actual = extract_page_data(input_body, input_url)

            expected = {
                "url": "https://crawler-test.com",
                "heading": "First Title",
                "first_paragraph": "This is the first paragraph.",
                "outgoing_links": [
                    "https://crawler-test.com/link1",
                    "https://crawler-test.com/link2",
                ],
                "image_urls": [
                    "https://crawler-test.com/image1.jpg",
                    "https://crawler-test.com/image2.jpg",
                ],
            }
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
