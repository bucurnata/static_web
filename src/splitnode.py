import re
from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown: missing closing delimiter{delimiter}")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(parts[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        imgs = extract_markdown_images(original_text)
        if not imgs:
            new_nodes.append(old_node)
            continue
        for alt, url in imgs:
            sections = original_text.split(f"![{alt}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            original_text = sections[1] if len(sections) > 1 else "" 
        if original_text.strip():
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
      

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if not links:
            new_nodes.append(old_node)
            continue
        for link, url in links:
            sections = original_text.split(f"[{link}]({url})",1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link, TextType.LINK, url))
            original_text = sections[1] if len(sections) > 1 else ""
        if original_text.strip():
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
        nodes = [TextNode(text, TextType.TEXT)]
        nodes = split_nodes_image(nodes)
        nodes = split_nodes_link(nodes)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        return nodes


