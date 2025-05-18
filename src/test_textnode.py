import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    #def test_link_node_with_missing_url_raises(self):
        #node = TextNode("Click here", TextType.LINK)
        #with self.assertRaises(Exception):
        #    text_node_to_html_node(node)

    #def test_image_node_with_missing_url_raises(self):
        #node = TextNode("A picture", TextType.IMAGE)
        #with self.assertRaises(Exception):
        #   text_node_to_html_node(node)

    def test_invalid_text_type_raises(self):
        class FakeType:
            pass
        node = TextNode("Invalid", FakeType)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_empty_text_value(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")
        self.assertIsNone(html_node.tag)

    def test_link_node_with_valid_url(self):
        node = TextNode("Click", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image_node_with_valid_url(self):
        node = TextNode("Alt text", TextType.IMAGE, url="img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "img.png", "alt": "Alt text"})

    def test_code_node_special_chars(self):
        node = TextNode("<script>", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "<script>")


if __name__ == "__main__":
    unittest.main()