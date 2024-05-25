from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        return (
            self.text == node.text
            and self.text_type == node.text_type
            and self.url == node.url
        )

    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type}, {self.url})'

def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError("No valid text_type provided")

def split_nodes_delimiter(old_nodes, delimiter, new_text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == "text":
            split_parts = node.text.split(delimiter)
            
            # Check for matching delimiters
            if len(split_parts) > 0 and len(split_parts) % 2 == 0:
                raise ValueError(f"Missing closing delimiter for {delimiter} in text: {node.text}")
            
            # Process and create new TextNodes
            for i, part in enumerate(split_parts):
                if i % 2 == 0:
                    if part:
                        new_nodes.append(TextNode(part, "text"))
                else:
                    new_nodes.append(TextNode(part, new_text_type))
        else:
            new_nodes.append(node)
    
    return new_nodes

