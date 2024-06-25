import unittest

from extract import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link

from textnode import (
        TextNode,
        text_type_text,
        text_type_bold,
        text_type_italic,
        text_type_code,
        text_type_link,
        text_type_image,
)
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
        node = TextNode("This is **bold** text", text_type_text)
        result = split_nodes_delimiter([node], "**", text_type_bold)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text", text_type_text)
        ]
        self.assertEqual(result, expected)

    def test_split_multiple_delimiters(self):
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
        node = TextNode("This is plain text", text_type_text)
        result = split_nodes_delimiter([node], "**", "bold")
        expected = [node]
        self.assertEqual(result, expected)

    def test_split_unmatched_delimiter(self):
        node = TextNode("This is **bold text", text_type_text)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", text_type_bold)

    def test_non_text_node(self):
        node = TextNode("This is plain text", "bold")
        result = split_nodes_delimiter([node], "**", "bold")
        expected = [node]
        self.assertEqual(result, expected)

    def test_mixed_node_types(self):
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

    def test_split_nodes_images_one(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            text_type_text
        )
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_images_two(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a ![second](http://storage.images.com)",
            text_type_text
        )
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("second", text_type_image, "http://storage.images.com"),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_images_image_beginning(self):
        node = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a text.",
            text_type_text
        )
        expected = [
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a text.", text_type_text),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_images_image_end(self):
        node = TextNode(
            "A text and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            text_type_text
        )
        expected = [
            TextNode("A text and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_images_only_text(self):
        node = TextNode(
            "Just a boring text.",
            text_type_text
        )
        expected = [
            TextNode("Just a boring text.", text_type_text),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_links_one(self):
        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            text_type_text
        )
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_links_two(self):
        node = TextNode(
            "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [second](http://storage.links.com)",
            text_type_text
        )
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("second", text_type_link, "http://storage.links.com"),
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_links_link_beginning(self):
        node = TextNode(
            "[link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a text.",
            text_type_text
        )
        expected = [
            TextNode("link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a text.", text_type_text),
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_links_link_end(self):
        node = TextNode(
            "A text and an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            text_type_text
        )
        expected = [
            TextNode("A text and an ", text_type_text),
            TextNode("link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_links_only_text(self):
        node = TextNode(
            "Just a boring text.",
            text_type_text
        )
        expected = [
            TextNode("Just a boring text.", text_type_text),
        ]
        self.assertEqual(split_nodes_link([node]), expected)

if __name__ == "__main__":
    unittest.main()

