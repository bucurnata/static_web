import unittest
from splitnode import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

from textnode import TextNode, TextType


class TestSplitNode(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_single_bold_block_only(self):
        node = TextNode("**just bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("just bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_multiple_code_blocks(self):
        node = TextNode("Check this `code block` out and this `other one` too", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("Check this ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" out and this ", TextType.TEXT),
                TextNode("other one", TextType.CODE),
                TextNode(" too", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_plain_text_unchanged(self):
        node = TextNode("Plain text with no special formatting", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [TextNode("Plain text with no special formatting", TextType.TEXT)],
            new_nodes,
        )

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This text has an **unmatched delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_multiple_nodes_input(self):
        node1 = TextNode("First **bold** text", TextType.TEXT)
        node2 = TextNode("Second text", TextType.TEXT)
        node3 = TextNode("Third **bold again** text", TextType.TEXT)
        result = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
                TextNode("Second text", TextType.TEXT),
                TextNode("Third ", TextType.TEXT),
                TextNode("bold again", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            result,
        )
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_basic_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
    )
    
    def test_split_links(self):
        node = TextNode(
            "This is a [link](https://example.com) and another [link2](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
    )
        
    
    def test_plain_text(self):
        text = "Just plain text with no formatting."
        expected = [TextNode("Just plain text with no formatting.", TextType.TEXT)]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_bold_text(self):
        text = "This is **bold** text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT)
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_italic_and_code(self):
        text = "An _italic_ word and `code` example."
        expected = [
            TextNode("An ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" example.", TextType.TEXT)
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_image_and_link(self):
        text = "Here is an image ![pic](https://img.com/pic.png) and a [link](https://example.com)."
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("pic", TextType.IMAGE, "https://img.com/pic.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_all_markdown_features(self):
        text = (
            "Start **bold** _italic_ `code` ![alt](img.png) [link](url.com) end."
        )
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "img.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(" end.", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_multiple_bold_blocks(self):
        text = "**one** and **two**"
        expected = [
            TextNode("one", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.BOLD)
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    

if __name__ == "__main__":
    unittest.main()
