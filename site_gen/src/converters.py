import enum
from htmlnode import LeafNode
from md_extrators import extract_markdown_images, extract_markdown_urls
from textnode import TextNode, TextType

BlockType = enum.Enum(
    "BlockType",
    ["PARAGRAPH", "HEADING", "CODE", "QUOTE", "UNORDERED_LIST", "ORDERED_LIST"],
)


def block_to_block_type(markdown_text: str):
    lines = markdown_text.split("\n")
    if markdown_text.startswith(("# ", "## ", "### ", "#### ")):
        return BlockType.HEADING
    if markdown_text.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if markdown_text.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if markdown_text.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text, tag=None)
        case TextType.BOLD:
            return LeafNode(value=text_node.text, tag="b")
        case TextType.ITALIC:
            return LeafNode(value=text_node.text, tag="i")
        case TextType.CODE:
            return LeafNode(value=text_node.text, tag="code")
        case TextType.LINK:
            return LeafNode(
                value=text_node.text, tag="a", props={"href": text_node.url}
            )
        case TextType.IMAGE_LINK:
            return LeafNode(
                value="", tag="img", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise Exception("Unsupported text type")


def split_nodes_delimiter(old_nodes, delimeter, text_type):
    new_nodes = []
    if len(old_nodes) == 0:
        return None
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        splits = node.text.split(delimeter)
        if len(splits) % 2 == 0:
            raise ValueError("Not a valid markdown syntax(couldn't find delimiter)")

        for i in range(len(splits)):
            if i % 2 == 0:
                new_nodes.append(TextNode(text=splits[i], text_type=TextType.TEXT))
            else:
                new_nodes.append(TextNode(text=splits[i], text_type=text_type))
    return new_nodes


def split_node_images(old_nodes):
    return split_md_links(old_nodes, is_image=True)


def split_node_links(old_nodes):
    return split_md_links(old_nodes, is_image=False)


def split_md_links(old_nodes, is_image=False):
    new_nodes = []
    if len(old_nodes) == 0:
        return None
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = (
            extract_markdown_images(node.text)
            if is_image
            else extract_markdown_urls(node.text)
        )
        if len(images) == 0:
            new_nodes.append(node)
            continue
        current_text = node.text
        for i, (alt, url) in enumerate(images):
            split_delim = f"![{alt}]({url})" if is_image else f"[{alt}]({url})"
            sections = current_text.split(split_delim, 1)
            og_node = TextNode(text=sections[0], text_type=TextType.TEXT)
            image_node = TextNode(
                text=alt,
                text_type=TextType.IMAGE_LINK if is_image else TextType.LINK,
                url=url,
            )
            should_skip_leading_empty = (
                i == 0 and len(images) == 1 and sections[0] == "" and sections[1] != ""
            )
            if not should_skip_leading_empty:
                new_nodes.append(og_node)

            if image_node.text != "":
                new_nodes.append(image_node)
            current_text = sections[1]
        if current_text != "":
            new_nodes.append(TextNode(text=current_text, text_type=TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    if text.count("**") % 2 != 0:
        raise ValueError("Not a valid markdown syntax(couldn't find delimiter)")
    if text.count("_") % 2 != 0:
        raise ValueError("Not a valid markdown syntax(couldn't find delimiter)")
    if text.count("`") % 2 != 0:
        raise ValueError("Not a valid markdown syntax(couldn't find delimiter)")

    text_node = TextNode(text, TextType.TEXT)
    split_links = split_node_links([text_node]) or []
    split_images = split_node_images(split_links) or []
    try:
        split_code = split_nodes_delimiter(split_images, "`", TextType.CODE) or []
    except ValueError:
        split_code = split_images

    try:
        split_bold = split_nodes_delimiter(split_code, "**", TextType.BOLD) or []
    except ValueError:
        split_bold = split_code

    try:
        split_italic = split_nodes_delimiter(split_bold, "_", TextType.ITALIC) or []
    except ValueError:
        split_italic = split_bold

    if len(split_italic) > 1:
        return [
            node
            for node in split_italic
            if not (node.text_type == TextType.TEXT and node.text == "")
        ]

    return split_italic


def markdown_to_blocks(markdown):
    splits = markdown.split("\n\n")
    sanitized = []
    for split in splits:
        s_split = split.strip()
        if len(s_split) > 0:
            sanitized.append(s_split)
    return sanitized
