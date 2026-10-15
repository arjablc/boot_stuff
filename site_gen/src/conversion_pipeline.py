from converters import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    text_node_to_html_node,
    text_to_textnodes,
)
from htmlnode import ParentNode
from textnode import TextNode, TextType


def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def block_to_code_node(block):
    code_text = "\n".join(block.split("\n")[1:-1]) + "\n"
    code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
    return ParentNode("pre", [code_node])


def block_to_heading(block):
    level = len(block) - len(block.lstrip("#"))
    return ParentNode(f"h{level}", text_to_children(block[level + 1 :]))


def block_to_quote(block):
    value = " ".join(line.lstrip("> ") for line in block.split("\n"))
    return ParentNode("blockquote", text_to_children(value))


def block_to_list(block, block_type):
    tag = "ul" if block_type == BlockType.UNORDERED_LIST else "ol"
    items = []
    for line in block.split("\n"):
        if block_type == BlockType.UNORDERED_LIST:
            value = line[2:]
        else:
            value = line.split(". ", 1)[1]
        items.append(ParentNode("li", text_to_children(value)))
    return ParentNode(tag, items)


def block_to_paragraph(block):
    return ParentNode("p", text_to_children(block.replace("\n", " ")))


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.CODE:
        return block_to_code_node(block)
    if block_type == BlockType.HEADING:
        return block_to_heading(block)
    if block_type == BlockType.QUOTE:
        return block_to_quote(block)
    if block_type in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
        return block_to_list(block, block_type)
    return block_to_paragraph(block)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
