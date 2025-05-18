import unittest
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode 

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_valid_initialization(self):
        child = LeafNode(tag=None, value="Hello")
        node = ParentNode(tag="div", children=[child])
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)

    def test_missing_tag_raises(self):
        child = LeafNode(tag=None, value="Hello")
        with self.assertRaises(ValueError):
            ParentNode(tag=None, children=[child])

    def test_missing_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="div", children=None)

    def test_to_html_single_child(self):
        child = LeafNode(tag=None, value="Hello")
        node = ParentNode(tag="div", children=[child])
        self.assertEqual(node.to_html(), "<div>Hello</div>")

    def test_to_html_multiple_children(self):
        child1 = LeafNode(tag=None, value="Hello")
        child2 = LeafNode(tag="strong", value=" World")
        node = ParentNode(tag="p", children=[child1, child2])
        self.assertEqual(node.to_html(), "<p>Hello<strong> World</strong></p>")

    def test_to_html_with_nested_tags(self):
        child = LeafNode(tag="span", value="Nested")
        node = ParentNode(tag="div", children=[child])
        self.assertEqual(node.to_html(), "<div><span>Nested</span></div>")

if __name__ == "__main__":
    unittest.main()
