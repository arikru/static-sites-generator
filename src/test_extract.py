import unittest

from extract import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from textnode import TextNode

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

    def test_split_simple(self):
        text_type_text = "text"
        text_type_bold = "bold"
        node = TextNode("This is **bold** text", text_type_text)
        result = split_nodes_delimiter([node], "**", text_type_bold)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text", text_type_text)
        ]
        self.assertEqual(result, expected)

    def test_split_multiple_delimiters(self):
        text_type_text = "text"
        text_type_bold = "bold"
        node = TextNode("This **is** a **test**", text_type_text)
        result = split_nodes_delimiter([node], "**", text_type_bold)
        expected = [
            TextNode("This ", text_type_text),
            TextNode("is", text_type_bold),
            TextNode(" a ", text_type_text),
            TextNode("test", text_type_bold)
        ]
        self.assertEqual(result, expected)

    def test_split_no_delimiters(self):
        text_type_text = "text"
        node = TextNode("This is plain text", text_type_text)
        result = split_nodes_delimiter([node], "**", "bold")
        expected = [node]
        self.assertEqual(result, expected)

    def test_split_unmatched_delimiter(self):
        text_type_text = "text"
        text_type_bold = "bold"
        node = TextNode("This is **bold text", text_type_text)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", text_type_bold)

    def test_non_text_node(self):
        text_type_text = "text"
        node = TextNode("This is plain text", "bold")
        result = split_nodes_delimiter([node], "**", "bold")
        expected = [node]
        self.assertEqual(result, expected)

    def test_mixed_node_types(self):
        text_type_text = "text"
        text_type_bold = "bold"
        node1 = TextNode("This is **bold** text", text_type_text)
        node2 = TextNode("Non-split text", "bold")
        result = split_nodes_delimiter([node1, node2], "**", text_type_bold)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text", text_type_text),
            node2
        ]
        self.assertEqual(result, expected)
if __name__ == "__main__":
    unittest.main()

