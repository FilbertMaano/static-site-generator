from textnode import *
from htmlnode import *

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    return re.split(r"\n{2,}", markdown.strip())


def block_to_block_type(block):
    if re.match(r"^#{1,6} .+$", block):
        return block_type_heading
    if re.match(r"^`{3}.+`{3}$", block, re.DOTALL):
        return block_type_code
    lines = block.split("\n")
    if all(map(lambda x: re.match(r"^> .+$", x), lines)):
        return block_type_quote
    if all(map(lambda x: re.match(r"^[*-] .+$", x), lines)):
        return block_type_unordered_list
    for i, line in enumerate(lines):
        if not re.match(rf"^{i+1}\. .+$", line):
            break
    else:
        return block_type_ordered_list

    return block_type_paragraph


def paragraph_block_to_html(paragraph_block):
    nodes = text_to_textnodes(paragraph_block)
    children = [node.text_node_to_html_node(node) for node in nodes]
    return ParentNode("p", children)


def heading_block_to_html(heading_block):
    nodes = text_to_textnodes(heading_block.strip("# \n"))
    children = [node.text_node_to_html_node(node) for node in nodes]
    return ParentNode(f"h{heading_block.count('#')}", children)


def code_block_to_html(code_block):
    code = code_block.strip("` \n")
    children = [LeafNode("code", code)]
    return ParentNode("pre", children)


def quote_block_to_html(quote_block):
    children = [
        paragraph_block_to_html(line.strip("> ")) for line in quote_block.split("\n")
    ]
    return ParentNode("blockquote", children)


def unordered_list_block_to_html(block):
    block = block.strip()
    children = []
    for line in block.split("\n"):
        line = line.strip("- \n")
        nodes = text_to_textnodes(line)
        children_2 = [node.text_node_to_html_node(node) for node in nodes]
        children.append(ParentNode("li", children_2))
    return ParentNode("ul", children)


def ordered_list_block_to_html(block):
    block = block.strip()
    children = []
    for line in block.split("\n"):
        line = re.sub(r"\d+. ", "", line).strip()
        nodes = text_to_textnodes(line)
        children_2 = [node.text_node_to_html_node(node) for node in nodes]
        children.append(ParentNode("li", children_2))
    return ParentNode("ol", children)


def markdown_to_htmlnode(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_paragraph:
            children.append(paragraph_block_to_html(block))
        elif block_type == block_type_heading:
            children.append(heading_block_to_html(block))
        elif block_type == block_type_code:
            children.append(code_block_to_html(block))
        elif block_type == block_type_quote:
            children.append(quote_block_to_html(block))
        elif block_type == block_type_unordered_list:
            children.append(unordered_list_block_to_html(block))
        elif block_type == block_type_ordered_list:
            children.append(ordered_list_block_to_html(block))
    return ParentNode("div", children)
