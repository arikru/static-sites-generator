import unittest

from block import (
        block_to_block_type,
        markdown_to_blocks,
        block_type_paragraph,
        block_type_heading,
        block_type_code,
        block_type_quote,
        block_type_unordered_list,
        block_type_ordered_list,
)

class TestInlineMarkdown(unittest.TestCase):
    def test_markdown_to_blocks_simple(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here

This is the same paragraph on a new line

* This is a list
* with items"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here",
            "This is the same paragraph on a new line",
            """* This is a list\n* with items"""
        ]
        result = markdown_to_blocks(md)
        self.assertListEqual(result, expected)

    def test_markdown_to_blocks_excessive_newline(self):
        md = """This is **bolded** paragraph\n\n\n\nThis is another paragraph with *italic* text and `code` here\n\n\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here",
            "This is the same paragraph on a new line",
            """* This is a list\n* with items"""
        ]
        result = markdown_to_blocks(md)
        self.assertListEqual(result, expected)

    def test_markdown_to_blocks_excessive_only_newline(self):
        md = """\n\n\n\n\n\n\n\n\n"""
        expected = []
        result = markdown_to_blocks(md)
        self.assertListEqual(result, expected)
        
    def test_block_to_block_type(self):
        md = "# I am a Heading"
        expected = block_type_heading
        result = block_to_block_type(md)
        self.assertEqual(result, expected)

    def test_block_to_block_type_2(self):
        md = "##    I am a Heading"
        expected = block_type_heading
        result = block_to_block_type(md)
        self.assertEqual(result, expected)

    def test_block_to_block_type_code(self):
        md = "```I am a code block```"
        expected = block_type_code
        result = block_to_block_type(md)
        self.assertEqual(result, expected)

    def test_block_to_block_type_quote(self):
        md = ">Line 1\n>Line 2"
        expected = block_type_quote
        result = block_to_block_type(md)
        self.assertEqual(result, expected)

    def test_block_to_block_type_ul_star(self):
        md = "* Line 1\n* Line 2"
        expected = block_type_unordered_list
        result = block_to_block_type(md)
        self.assertEqual(result, expected)

    def test_block_to_block_type_ul_hyphen(self):
        md = "- Line 1\n- Line 2"
        expected = block_type_unordered_list
        result = block_to_block_type(md)
        self.assertEqual(result, expected)

    def test_block_to_block_type_ol(self):
        md = "1. Line 1\n2. Line 2"
        expected = block_type_ordered_list
        result = block_to_block_type(md)
        self.assertEqual(result, expected)
