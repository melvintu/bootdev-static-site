from enum import Enum
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LISTS = "unordered_lists"
    ORDERED_LISTS = "ordered_lists"

def block_to_block_type(block):
    lines = block.splitlines()

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if len(lines) > 1 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LISTS
    
    if block.startswith("1. "):
        current_count = 1
        for line in lines:
            if not line.startswith(f"{current_count}. "):
                return BlockType.PARAGRAPH
            current_count +=1 
        return BlockType.ORDERED_LISTS
    
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    split_md = markdown.split("\n\n")
    blocked_md = []
    for block in split_md:
        block = block.strip()
        if block != "":
            blocked_md.append(block)

    return blocked_md