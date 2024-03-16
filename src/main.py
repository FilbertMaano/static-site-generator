from textnode import TextNode
from htmlnode import *

print(TextNode("This is a text node", "bold", "https://www.boot.dev"))

node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        ),
        LeafNode(None, "Normal text"),
    ],
)

print(node.to_html())
