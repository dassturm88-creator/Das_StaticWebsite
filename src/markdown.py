import re
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT and delimiter in node.text:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError("Delimiter split resulted in an even number of parts, which is unexpected.")
            for i, part in enumerate(parts):
                if not part:
                    continue

                if i % 2 == 0:
                    new_nodes.append(TextNode(part, node.text_type, node.url))
                else:
                    new_nodes.append(TextNode(part, text_type, node.url))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            if images:
                last_index = 0
                for alt_text, url in images:
                    start_index = node.text.find(f"![{alt_text}]({url})", last_index)
                    if start_index > last_index:
                        new_nodes.append(TextNode(node.text[last_index:start_index], TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                    last_index = start_index + len(f"![{alt_text}]({url})")
                if last_index < len(node.text):
                    new_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            if links:
                last_index = 0
                for link_text, url in links:
                    start_index = node.text.find(f"[{link_text}]({url})", last_index)
                    if start_index > last_index:
                        new_nodes.append(TextNode(node.text[last_index:start_index], TextType.TEXT))
                    new_nodes.append(TextNode(link_text, TextType.LINK, url))
                    last_index = start_index + len(f"[{link_text}]({url})")
                if last_index < len(node.text):
                    new_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def markdown_to_blocks(markdown_text: str) -> list[str]:
    lines = markdown_text.split("\n\n")
    blocks = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:  
            blocks.append(stripped_line)
    return blocks

def block_to_block_type(block):
    count = 0
    for character in block:
        if character != "#":
            break
        count += 1
    if 1 <= count <= 6 and len(block) > count and block[count] == " ":
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    expected_number = 1
    for line in lines:
        prefix = f"{expected_number}. "
        if not line.startswith(prefix):
            break
        expected_number += 1
    else:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            paragraph_text = " ".join(block.split("\n"))
            paragraph_children = text_to_children(paragraph_text)
            children.append(ParentNode("p", paragraph_children))
        elif block_type == BlockType.CODE:
            code_text = block[4:-3]
            text_node = TextNode(code_text, TextType.TEXT)
            code_html_node = text_node_to_html_node(text_node)
            code_node = ParentNode("code", [code_html_node])
            pre_node = ParentNode("pre", [code_node])
            children.append(pre_node)
        elif block_type == BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            heading_text = block[level + 1:]
            heading_children = text_to_children(heading_text)
            children.append(ParentNode(f"h{level}", heading_children))
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(line.lstrip(">").strip())
            content = " ".join(new_lines)
            quote_children = text_to_children(content)
            children.append(ParentNode("blockquote", quote_children))
        elif block_type == BlockType.UNORDERED_LIST:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                text = item[2:] 
                li_nodes.append(ParentNode("li", text_to_children(text)))
            children.append(ParentNode("ul", li_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                text = item.split(". ", 1)[1] 
                li_nodes.append(ParentNode("li", text_to_children(text)))
            children.append(ParentNode("ol", li_nodes))
    return ParentNode("div", children)

def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children