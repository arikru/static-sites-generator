class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        if (self.text == node.text
            and self.text_type == node.text
            and self.url == node.url
        ):
            return True
        else:
            return False

    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
