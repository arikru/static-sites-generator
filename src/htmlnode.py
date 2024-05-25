class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        attributes = " "

        for k,v in self.props.items():
            attributes += f'{k}=\"{v}\" '
        
        return attributes.rstrip()

    def __repr__(self) -> str:
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props}'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node requires a value")
        if self.tag is None:
            return str(self.value)
        if self.props is None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag of ParentNode cannot be None value")
        if self.children is None:
            raise ValueError("ParentNode cannot have no children (None provided)")

        parsed_nodes = []

        for child in self.children:
            parsed_nodes.append(child.to_html())
        return f'<{self.tag}>{"".join(parsed_nodes)}</{self.tag}>'
