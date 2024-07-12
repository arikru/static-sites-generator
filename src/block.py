import re

from htmlnode import HTMLNode, ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered list"


def markdown_to_blocks(markdown):
    blank_line_regex = r"(?:\r?\n){2,}"
    blocks = re.split(blank_line_regex, markdown.strip())
    return list(filter(None, blocks))


def block_to_block_type(block):
    # Headings
    headings_pattern = re.compile(r'^\s*(#{1,6})\s+(.+)$', re.MULTILINE)
    headings = headings_pattern.findall(block)

    if headings:
        return block_type_heading

    # Code
    split = block.split('```')

    if split[0] == '' and split[-1] == '':
        return block_type_code

    # Quote
    split = block.split('\n')
    quote = True

    for line in split:
        if len(line) == 0 or line[0] != ">":
            quote = False
            break

    if quote:
        return block_type_quote

    # Unordered list
    ul = True

    for line in split:
        if len(line) == 0 or (line[:2] != "* " and line[:2] != "- "):
            ul = False
            break

    if ul:
        return block_type_unordered_list

    # Ordered list
    ol = True
    seq = []

    for line in split:
        if len(line) > 0 and line[0].isdigit():
            seq.append(int(line[0]))
        else:
            ol = False
            break

    if ol and seq == list(range(1, len(seq) + 1)):
        for line in split:
            if line[1:3] != ". ":
                ul = False
                break

    if ol:
        return block_type_ordered_list

    return block_type_paragraph


def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == block_type_paragraph:
            node = convert_paragraph_block(block)

        if block_type == block_type_quote:
            node = convert_quote_block(block)

        if block_type == block_type_code:
            node = convert_code_block(block)

        if block_type == block_type_heading:
            node = convert_heading_block(block)

        if block_type == block_type_unordered_list:
            node = convert_unordered_block(block)

        if block_type == block_type_ordered_list:
            node = convert_ordered_block(block)

        nodes.append(node)

    return ParentNode("div", nodes)


def convert_paragraph_block(block):
    return HTMLNode("<p>", block)


def convert_quote_block(block):
    return HTMLNode("<blockquote>", block[1:])


def convert_code_block(block):
    return HTMLNode("<code>", block[3:-3])


def convert_heading_block(block):
    h_nr = len(block.split()[0])
    return HTMLNode(f"<h{h_nr}>", block[h_nr:])


def convert_unordered_block(block):
    items = []
    lines = block.splitlines()
    for line in lines:
        items.append(f"<li>{line[2:]}</li>")
    return items


def convert_ordered_block(block):
    ...
