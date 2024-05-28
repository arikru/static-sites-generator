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

    for node in old_nodes:
        if node.text_type == text_type_text:
            split_parts = node.text.split(delimiter)
            
            # Check for matching delimiters
            if len(split_parts) > 0 and len(split_parts) % 2 == 0:
                raise ValueError(f"Missing closing delimiter for {delimiter} in text: {node.text}")
            
            # Process and create new TextNodes
            for i, part in enumerate(split_parts):
                if i % 2 == 0:
                    if part:
                        new_nodes.append(TextNode(part, text_type_text))
                else:
                    new_nodes.append(TextNode(part, new_text_type))
        else:
            new_nodes.append(node)
    
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
