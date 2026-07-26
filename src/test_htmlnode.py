import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "my-class"})

    def test_props_to_html_with_props(self):
        node = HTMLNode(tag="div", props={"class": "my-class", "id": "my-id"})
        expected_html = ' class="my-class" id="my-id"'
        self.assertEqual(node.props_to_html(), expected_html)

    def test_props_to_html_without_props(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_init(self):
        leaf = LeafNode(tag="span", value="Hello", props={"class": "my-class"})
        self.assertEqual(leaf.tag, "span")
        self.assertEqual(leaf.value, "Hello")
        self.assertIsNone(leaf.children)
        self.assertEqual(leaf.props, {"class": "my-class"})

    def test_to_html_with_tag_and_value(self):
        leaf = LeafNode(tag="span", value="Hello", props={"class": "my-class"})
        expected_html = '<span class="my-class">Hello</span>'
        self.assertEqual(leaf.to_html(), expected_html)

    def test_to_html_without_tag(self):
        leaf = LeafNode(tag=None, value="Hello")
        expected_html = 'Hello'
        self.assertEqual(leaf.to_html(), expected_html)

    def test_to_html_without_value(self):
        leaf = LeafNode(tag="span", value=None)
        with self.assertRaises(ValueError):
            leaf.to_html()

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

    def test_to_html_without_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(tag=None, children=[child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_without_children(self):
        parent_node = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_init(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(tag="div", children=[child_node], props={"class": "my-class"})
        self.assertEqual(parent_node.tag, "div")
        self.assertIsNone(parent_node.value)
        self.assertEqual(parent_node.children, [child_node])
        self.assertEqual(parent_node.props, {"class": "my-class"})

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(tag="div", children=[child_node], props={"class": "my-class"})
        expected_html = '<div class="my-class"><span>child</span></div>'
        self.assertEqual(parent_node.to_html(), expected_html)
    
    def test_to_html_without_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(tag="div", children=[child_node])
        expected_html = '<div><span>child</span></div>'
        self.assertEqual(parent_node.to_html(), expected_html)

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode(tag="div", children=[child_node1, child_node2])
        expected_html = '<div><span>child1</span><span>child2</span></div>'
        self.assertEqual(parent_node.to_html(), expected_html)  
    
    def test_to_html_with_nested_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        expected_html = '<div><span><b>grandchild</b></span></div>'
        self.assertEqual(parent_node.to_html(), expected_html)
    
    def test_to_html_with_nested_children_and_props(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node], props={"class": "child-class"})
        parent_node = ParentNode("div", [child_node], props={"id": "parent-id"})
        expected_html = '<div id="parent-id"><span class="child-class"><b>grandchild</b></span></div>'
        self.assertEqual(parent_node.to_html(), expected_html)  
    
    def test_to_html_with_multiple_nested_children(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("i", "grandchild2")
        child_node1 = ParentNode("span", [grandchild_node1])
        child_node2 = ParentNode("span", [grandchild_node2])
        parent_node = ParentNode("div", [child_node1, child_node2])
        expected_html = '<div><span><b>grandchild1</b></span><span><i>grandchild2</i></span></div>'
        self.assertEqual(parent_node.to_html(), expected_html)
