from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode requires a tag")
        if children is None:
            raise ValueError("ParentNode requires children")
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires a tag")
        if self.children is None:
            raise ValueError("ParentNode requires children")
        nodes = ""
        for node in self.children:
            nodes += node.to_html()
        return f"<{self.tag}>{nodes}</{self.tag}>"
