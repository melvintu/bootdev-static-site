from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
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
        children_nodes = text_to_children(text)
        return ParentNode("blockquote", children_nodes)
    
    if block_type == BlockType.UNORDERED_LISTS:
        tagged_list = tagging_lines_in_list(text)
        return ParentNode("ul", tagged_list)
    
    if block_type == BlockType.ORDERED_LISTS:
        tagged_list = tagging_lines_in_list(text)
        return ParentNode("ol", tagged_list)
    
    if block_type == BlockType.CODE:
        children_nodes = text_to_children(text)
        parent_node = ParentNode("pre", children_nodes)
        return ParentNode("code", parent_node)

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
        child_node = text_to_children(line)
        tagged_list.append(ParentNode("li", child_node))
    return tagged_list

# Takes block -> Turns block and splits it into TextNodes
# Takes each Textnode and turns it into a LeafNode
# The LeafNodes are then attached to the ParentNode (Which is the block)
# The block is then attached to the main GrandparentNode(Another parent node)
# Structure LeafNode (The individual lines of text)
# -> ParentNode (The block nodes)
# -> GrandparentNode (The Body)

#Unordered lists, need to be ParentNode(Block for ul) -> Each line is li -> LeafNode
# Unordered list text needs to be first split into a list
# So it looks like ["- number 1", "- number 2", "- number **3**"]
# Then each item in the list gets put through the nodes, then put through li tag, then put through ul tag

#notes - Child node = leaf node, where LeafNode(the tag (span), "the content")
# then parent node is ParentNode(tag(div), [child_node])
# then whath appens is parent_node.to_html() becomes <div><span>child</span></div>