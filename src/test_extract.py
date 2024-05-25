import unittest

from extract import extract_markdown_images, extract_markdown_links

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [
            ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
        ]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_extract_markdown_images_empty(self):
        text = "This is text with no images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another")
        ]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_extract_markdown_links_empty(self):
        text = "This is text with no links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

if __name__ == "__main__":
    unittest.main()

