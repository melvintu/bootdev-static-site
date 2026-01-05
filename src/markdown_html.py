from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        print(block)
        block_type = block_to_block_type(block)
        print(block_type)

        #if block_type == BlockType.HEADING:
            #heading_count = heading_tag_count(block)
            

def heading_tag_count(block):
    i = 0
    for character in block:
        if character != "#":
            break
        i += 1
    return f"h{i}"

def text_to_children(text):
    pass