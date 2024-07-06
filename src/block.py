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
        if line[0] != ">":
            quote = False
            break

    if quote:
        return block_type_quote

    # Unordered list
    ul = True

    for line in split:
        if line[:2] != "* " and line[:2] != "- ":
            ul = False
            break

    if ul:
        return block_type_unordered_list

    # Ordered list
    ol = True

    seq = [int(line[0]) for line in split]

    if seq != list(range(1, len(seq) + 1)):
        ol = False
    else:
        for line in split:
            if line[1:3] != ". ":
                ul = False
                break

    if ol:
        return block_type_ordered_list

    return block_type_paragraph
