import unittest
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from markdown import text_to_text_nodes

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_eq_different_type_and_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_text_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_text_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_text_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_text_image(self):
        node = TextNode("This is an image text node", TextType.IMAGE, "https://www.example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.example.com/image.png", "alt": "This is an image text node"})    

    def test_text_link_without_url(self):
        node = TextNode("This is a link text node", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_text_image_without_url(self):
        node = TextNode("This is an image text node", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_text_unsupported_type(self):
        class UnsupportedTextType(Enum):
            UNSUPPORTED = "unsupported"
        node = TextNode("This is an unsupported text node", UnsupportedTextType.UNSUPPORTED)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_text_to_text_nodes(self):
        text = "This is a text node"
        text_type = TextType.TEXT
        url = None
        expected_nodes = [TextNode(text, text_type, url)]
        self.assertEqual(text_to_text_nodes(text), expected_nodes)

if __name__ == "__main__":
    unittest.main()