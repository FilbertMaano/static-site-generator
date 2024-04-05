import re
from htmlnode import LeafNode, ParentNode

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

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        if self.url is None:
            return f"TextNode({self.text}, {self.text_type})"
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_node_to_html_node(self, text_node):
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
        raise ValueError(f"Invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if type(old_node) != TextNode:
            new_nodes.append(old_node)
            continue
        if old_node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Closing delimeter for {delimiter} is not found.")
        nodes = old_node.text.split(delimiter)
        text = old_node.text.strip()
        for node in nodes:
            if f"{delimiter}{node}{delimiter}" in text:
                new_nodes.append(TextNode(node, text_type))
                text = text.replace(f"{delimiter}{node}{delimiter}", node)
            else:
                new_nodes.append(TextNode(node, old_node.text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images_tup = extract_markdown_images(old_node.text)
        if len(images_tup) == 0:
            new_nodes.append(old_node)
            continue
        text = old_node.text.strip()
        for i, image_tup in enumerate(images_tup):
            alt, link = image_tup
            texts = text.split(f"![{alt}]({link})", 1)
            if texts[0] != "":
                new_nodes.append(TextNode(texts[0], text_type_text))
            new_nodes.append(TextNode(alt, text_type_image, link))
            text = texts[-1]
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links_tup = extract_markdown_links(old_node.text)
        if len(links_tup) == 0:
            new_nodes.append(old_node)
            continue
        text = old_node.text.strip()
        for i, link_tup in enumerate(links_tup):
            alt, link = link_tup
            texts = text.split(f"[{alt}]({link})", 1)
            if texts[0] != "":
                new_nodes.append(TextNode(texts[0], text_type_text))
            new_nodes.append(TextNode(alt, text_type_link, link))
            text = texts[-1]
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes


def text_to_textnodes(text):
    textnodes = [TextNode(text, text_type_text)]
    textnodes = split_nodes_delimiter(textnodes, "**", text_type_bold)
    textnodes = split_nodes_delimiter(textnodes, "*", text_type_italic)
    textnodes = split_nodes_delimiter(textnodes, "`", text_type_code)
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_link(textnodes)
    return textnodes
