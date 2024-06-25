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

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == text_type_text:
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
