import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_simple_tag(self):
        node = LeafNode("p", "Hello world")
        self.assertEqual(node.to_html(), "<p>Hello world</p>")

    def test_tag_with_props(self):
        node = LeafNode("a", "Click me", {"href": "https://example.com", "target": "_blank"})
        expected = '<a href="https://example.com" target="_blank">Click me</a>'
        self.assertEqual(node.to_html(), expected)

    def test_no_children_allowed(self):
        # Verify children can't be passed (compile-time check)
        # This would actually be a syntax error if uncommented:
        # node = LeafNode("div", "content", children=["not allowed"])
        
        # Runtime verification that children is always None
        node = LeafNode("div", "content")
        self.assertIsNone(node.children)

   # def test_void_element_handling(self):
        # For elements like <img> where content isn't allowed
        #node = LeafNode("img", "", {"src": "image.jpg", "alt": "image"})
        #self.assertEqual(node.to_html(), '<img src="image.jpg" alt="image">')


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )    





if __name__ == "__main__":
    unittest.main()