import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered list"

def markdown_to_blocks(markdown):
        blank_line_regex = r"(?:\r?\n){2,}"
        blocks= re.split(blank_line_regex, markdown.strip())
        return list(filter(None, blocks))

def block_to_block_type(block):
    headings_pattern = re.compile(r'^\s*(#{1,6})\s+(.+)$', re.MULTILINE)
    headings = headings_pattern.findall(block)
    if headings:
        return block_type_heading
