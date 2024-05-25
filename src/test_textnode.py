import unittest

from textnode import TextNode, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_single_none(self):
        node = TextNode("This is a text node", "bold", url=None)
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is another text node", "bold")
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

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

