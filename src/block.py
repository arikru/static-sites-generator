import re
from types import new_class

from htmlnode import HTMLNode, ParentNode
from extract import text_to_textnodes
from textnode import text_node_to_html_node

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
    split = block.split('\n')

    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading

    # Code
    if len(split) > 1 and split[0].startswith("```") and split[-1].startswith("```"):
        return block_type_code

    # Quote
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
        node = block_to_html_node(block)
        nodes.append(node)

    return ParentNode("div", nodes, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return convert_paragraph_block(block)

    if block_type == block_type_quote:
        return convert_quote_block(block)

    if block_type == block_type_code:
        return convert_code_block(block)

    if block_type == block_type_heading:
        return convert_heading_block(block)

    if block_type == block_type_unordered_list:
        return convert_unordered_block(block)

    if block_type == block_type_ordered_list:
        return convert_ordered_block(block)
    raise ValueError("No valid block type")

def convert_paragraph_block(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def convert_quote_block(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def convert_code_block(block):
    if not block.startswith("```") or block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def convert_heading_block(block):
    h_nr = len(block.split()[0])
    text = block[h_nr+1:]
    children = text_to_children(text)
    return ParentNode(f"h{h_nr}", children)


def convert_unordered_block(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)


def convert_ordered_block(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
