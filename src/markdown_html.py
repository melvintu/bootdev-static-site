from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        block_node = block_to_parent(block)
        children_nodes.append(block_node)
    return ParentNode("div", children_nodes)

def block_to_parent(text):
    block_type = block_to_block_type(text)
    if block_type == BlockType.QUOTE:
        cleaned_text = clean_text_blockquotes(text)
        children_nodes = text_to_children(cleaned_text)
        return ParentNode("blockquote", children_nodes)
    
    if block_type == BlockType.UNORDERED_LISTS:
        tagged_list = tagging_lines_in_list(text)
        return ParentNode("ul", tagged_list)
    
    if block_type == BlockType.ORDERED_LISTS:
        tagged_list = tagging_lines_in_list(text)
        return ParentNode("ol", tagged_list)
    
    if block_type == BlockType.CODE:
        inner = strip_code_fence(text)
        code_text_node = TextNode(inner, TextType.CODE)
        code_html_node = text_node_to_html_node(code_text_node)
        return ParentNode("pre", [code_html_node])

    if block_type == BlockType.HEADING:
        header_tag_count = heading_tag_count(text)
        snipped_text = text[header_tag_count+1:]
        children_nodes = text_to_children(snipped_text)
        return ParentNode(f"h{header_tag_count}", children_nodes)

    if block_type == BlockType.PARAGRAPH:
        new_text = text.replace("\n", " ")
        children_nodes = text_to_children(new_text)
        return ParentNode("p", children_nodes)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes
    
def heading_tag_count(block):
    i = 0
    for character in block:
        if character != "#":
            break
        i += 1
    return i

def tagging_lines_in_list(text):
    split_lines = text.splitlines()
    if split_lines[0] == "":
        split_lines.pop(0)
    tagged_list = []
    for line in split_lines:
        if line.startswith("-"):
            new_line = line[2:]
        else:
            new_line = line[3:]
        child_node = text_to_children(new_line)
        tagged_list.append(ParentNode("li", child_node))
    return tagged_list

def clean_text_blockquotes(text):
    lines = [line for line in text.splitlines() if line.strip() !=""]
    pieces = []
    for line in lines:
        if line.startswith("> "):
            pieces.append(line[2:])
        elif line.startswith(">"):
            pieces.append(line[1:].lstrip())
        else:
            pieces.append(line)
    return " ".join(pieces)

def strip_code_fence(block):
    lines = block.split("\n")
    while lines and lines[0].strip() == "":
        lines.pop(0)
    while lines and lines[-1].strip() == "":
        lines.pop()
    if lines and lines[0].startswith("```"):
        lines.pop(0)
    if lines and lines[-1].startswith("```"):
        lines.pop()
    return "\n".join(lines) + "\n"
