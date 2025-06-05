import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node
)
from markdown_blocks import BlockType


class TestMarkdownBlocks(unittest.TestCase):
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_code_block(self):
        code = "```\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_quote_block(self):
        quote = "> This is a quote\n> Spanning multiple lines"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

    def test_unordered_list(self):
        ul = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(ul), BlockType.ULIST)

    def test_ordered_list(self):
        ol = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(ol), BlockType.OLIST)

    def test_invalid_ordered_list(self):
        bad_ol = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(bad_ol), BlockType.PARAGRAPH)

    def test_invalid_unordered_list(self):
        bad_ul = "- Item 1\n* Not valid"
        self.assertEqual(block_to_block_type(bad_ul), BlockType.PARAGRAPH)

    def test_paragraph(self):
        para = "This is a regular paragraph with no special syntax."
        self.assertEqual(block_to_block_type(para), BlockType.PARAGRAPH)

    def test_mixed_block(self):
        mixed = "> Quote line\nRegular line"
        self.assertEqual(block_to_block_type(mixed), BlockType.PARAGRAPH)

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        markdown = "## Heading Text"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.children[0].tag, "h2")
        self.assertEqual(result.children[0].children[0].value, "Heading Text")


    def test_ordered_list(self):
        markdown = "1. First item\n2. Second item"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.children[0].tag, "ol")
        self.assertEqual(result.children[0].children[0].tag, "li")
        self.assertEqual(result.children[0].children[0].children[0].value, "First item")
        self.assertEqual(result.children[0].children[1].children[0].value, "Second item")

    def test_unordered_list(self):
        markdown = "- Item A\n- Item B"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.children[0].tag, "ul")
        self.assertEqual(result.children[0].children[0].children[0].value, "Item A")
        self.assertEqual(result.children[0].children[1].children[0].value, "Item B")

    def test_quote_block(self):
        markdown = "> Line one\n> Line two"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.children[0].tag, "blockuote")
        self.assertEqual(result.children[0].children[0].value, "Line one Line two")

if __name__ == "__main__":
    unittest.main()