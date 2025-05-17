import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node1 = TextNode("Test text", TextType.TEXT)
        node2 = TextNode("Different text", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_not_eq_type(self):
        node1 = TextNode("Test text", TextType.TEXT)
        node2 = TextNode("Test text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_eq_with_url(self):
        node1 = TextNode("Test text", TextType.LINK, "https://example.com")
        node2 = TextNode("Test text", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)

    def test_not_eq_url(self):
        node1 = TextNode("Test text", TextType.LINK, "https://example.com")
        node2 = TextNode("Test text", TextType.LINK, "https://different.com")
        self.assertNotEqual(node1, node2)

    def test_url_none(self):
        node1 = TextNode("Test text", TextType.TEXT)
        node2 = TextNode("Test text", TextType.TEXT, None)
        self.assertEqual(node1, node2)

    def test_repr(self):
        node = TextNode("Test text", TextType.ITALIC, "https://example.com")
        self.assertEqual(
            repr(node),
            "TextNode(Test text, italic, https://example.com)"
        )

    def test_repr_with_none_url(self):
        node = TextNode("Test text", TextType.CODE)
        self.assertEqual(
            repr(node),
            "TextNode(Test text, code, None)"
        )

if __name__ == "__main__":
    unittest.main()