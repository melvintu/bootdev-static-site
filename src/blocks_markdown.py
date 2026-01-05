def markdown_to_blocks(markdown):
    split_md = markdown.split("\n\n")
    blocked_md = []
    for block in split_md:
        if block != '':
            blocked_md.append(block.strip())

    return blocked_md