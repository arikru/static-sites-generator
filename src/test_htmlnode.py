import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        prop_test =  " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), prop_test)

    def test_to_html_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        render = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), render)

    def test_to_html_no_tag(self):
        node = LeafNode(None, "I am so alone")
        render = "I am so alone"
        self.assertEqual(node.to_html(), render)

    def test_to_html_one_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        render = "<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(node.to_html(), render)

    def test_to_html_multiple_prop(self):
        node = LeafNode("a", "Click me", props={"href": "https://www.google.com", "target": "_blank"})
        render = "<a href=\"https://www.google.com\" target=\"_blank\">Click me</a>"
        self.assertEqual(node.to_html(), render)
