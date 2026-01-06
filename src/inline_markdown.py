import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    #print("split_nodes_delimiter", delimiter)
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        split_text = node.text.split(delimiter)
        #print("## This is split text inside split nodes##", split_text)
        if len(split_text)%2 == 0:
            raise Exception("Invalid markdown syntax: delimiter was not closed")
        for i in range(0, len(split_text)):
            if split_text[i] != "":
                if i%2 == 0:
                    split_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(split_text[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        remaining_text = node.text
        image_links = extract_markdown_images(node.text)
        if image_links == []:
            new_nodes.append(node)
            continue
        for tuple in image_links:
            alt, url = tuple
            split_text = remaining_text.split(f"![{alt}]({url})", 1)
            if len(split_text) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if split_text[0] != "":
                split_nodes.append(TextNode(split_text[0], TextType.TEXT))
            split_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = split_text[1]
        if remaining_text != "":
            split_nodes.append(TextNode(remaining_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        remaining_text = node.text
        url_link = extract_markdown_links(node.text)
        if url_link == []:
            new_nodes.append(node)
            continue
        for tuple in url_link:
            alt, url = tuple
            split_text = remaining_text.split(f"[{alt}]({url})", 1)
            if len(split_text) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if split_text[0] != "":
                split_nodes.append(TextNode(split_text[0], TextType.TEXT))
            split_nodes.append(TextNode(alt, TextType.LINK, url))
            remaining_text = split_text[1]
        if remaining_text != "":
            split_nodes.append(TextNode(remaining_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_link(nodes)
    return nodes