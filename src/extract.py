import re

from textnode import (
        TextNode,
        text_type_text,
        text_type_bold,
        text_type_italic,
        text_type_code,
        text_type_link,
        text_type_image,
)


def split_nodes_delimiter(old_nodes, delimiter, new_text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], new_text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    # Regex pattern to match markdown images
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    # Regex pattern to match markdown links
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        text = node.text

        for image_tup in images:
            split_parts = text.split(f"![{image_tup[0]}]({image_tup[1]})",1)
            if len(split_parts) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if split_parts[0] != "":
                new_nodes.append(TextNode(split_parts[0], text_type_text))

            new_nodes.append(TextNode(
                image_tup[0], 
                text_type_image, 
                image_tup[1]))


            text = split_parts[1]

        if text != "":
            new_nodes.append(TextNode(text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        if node.text_type == text_type_text:
            links = extract_markdown_links(node.text)
            if not links:
                new_nodes.append(node)
                continue

            text = node.text

            for link_tup in links:
                split_parts = text.split(f"[{link_tup[0]}]({link_tup[1]})",1)
                if len(split_parts) != 2:
                    raise ValueError("Invalid markdown, link section not closed")
                if split_parts[0] != "":
                    new_nodes.append(TextNode(split_parts[0], text_type_text))

                new_nodes.append(TextNode(
                    link_tup[0], 
                    text_type_link, 
                    link_tup[1]))


                text = split_parts[1]

            if text != "":
                new_nodes.append(TextNode(text, text_type_text))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
