class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        attbr_txt = ""
        for key, value in self.props.items():
            attbr_txt += f' {key}="{value}"'
        return attbr_txt

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props_to_html()})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(value=value, tag=tag, props=props)

    def to_html(self):
        if self.value is None:
            print(f"failing_html_node: {self}")
            raise ValueError()
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props_to_html()})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag")
        if len(self.children) == 0:
            raise ValueError("No children")
        children_html = ""
        for child in self.children:
            child_html = child.to_html()
            children_html += child_html
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
