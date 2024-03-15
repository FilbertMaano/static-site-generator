class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html is not yet implemented")

    def props_to_html(self):
        if self.props is None:
            return
        s = ""
        for key, value in self.props.items():
            s += f' {key}="{value}"'
        return s

    def __repr__(self) -> str:
        print("---HTML Node---")
        print(f"tag: {self.tag}")
        print(f"value: {self.value}")
        print(f"children: {self.children}")
        print(f"props: {self.props}")
        print("---END---")
