import unittest
from markdown import BlockType, block_to_block_type, markdown_to_blocks, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, markdown_to_html_node
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [
            TextNode("This is a text node with **bold** text.", TextType.TEXT),
            TextNode("This is another text node.", TextType.TEXT),
        ]
        delimiter = "**"
        text_type = TextType.BOLD

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        expected_nodes = [
            TextNode("This is a text node with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
            TextNode("This is another text node.", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)
    def test_split_nodes_delimiter_no_delimiter(self):
        old_nodes = [
            TextNode("This is a text node without delimiter.", TextType.TEXT),
            TextNode("This is another text node.", TextType.TEXT),
        ]
        delimiter = "**"
        text_type = TextType.BOLD

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        expected_nodes = [
            TextNode("This is a text node without delimiter.", TextType.TEXT),
            TextNode("This is another text node.", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)
    def test_split_nodes_delimiter_unmatched_delimiter(self):
        old_nodes = [
            TextNode("This is a text node with ** unmatched delimiter.", TextType.TEXT),
        ]
        delimiter = "**"
        text_type = TextType.BOLD

        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_extract_markdown_images(self):
        text = "Here is an image: ![alt text](image_url)"
        expected = [("alt text", "image_url")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_extract_markdown_images_with_multiple_images(self):
        text = "Here are multiple images: ![alt1](url1) and ![alt2](url2)"
        expected = [("alt1", "url1"), ("alt2", "url2")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_with_no_images(self):
        text = "This text has no images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "Here is a link: [link text](link_url)"
        expected = [("link text", "link_url")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_extract_markdown_links_with_exclamation(self):
        text = "Here is an image: ![alt text](image_url) and a link: [link text](link_url)"
        expected = [("link text", "link_url")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_with_multiple_links(self):
        text = "Here are multiple links: [link1](url1) and [link2](url2)"
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_split_nodes_image(self):
        old_nodes = [
            TextNode("This is a text node with an image ![alt text](image_url).", TextType.TEXT),
            TextNode("This is another text node.", TextType.TEXT),
        ]

        new_nodes = split_nodes_image(old_nodes)

        expected_nodes = [
            TextNode("This is a text node with an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "image_url"),
            TextNode(".", TextType.TEXT),
            TextNode("This is another text node.", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_no_images(self):
        old_nodes = [
            TextNode("This is a text node without images.", TextType.TEXT),
            TextNode("This is another text node.", TextType.TEXT),
        ]

        new_nodes = split_nodes_image(old_nodes)

        expected_nodes = [
            TextNode("This is a text node without images.", TextType.TEXT),
            TextNode("This is another text node.", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_image_with_multiple_images(self):
        old_nodes = [
            TextNode("This is a text node with multiple images ![alt1](url1) and ![alt2](url2).", TextType.TEXT),
        ]

        new_nodes = split_nodes_image(old_nodes)

        expected_nodes = [
            TextNode("This is a text node with multiple images ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "url2"),
            TextNode(".", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_image_with_image_at_start_and_end(self):
        old_nodes = [
            TextNode("![start](url_start) This is a text node with an image ![middle](url_middle) and another image ![end](url_end).", TextType.TEXT),
        ]

        new_nodes = split_nodes_image(old_nodes)

        expected_nodes = [
            TextNode("start", TextType.IMAGE, "url_start"),
            TextNode(" This is a text node with an image ", TextType.TEXT),
            TextNode("middle", TextType.IMAGE, "url_middle"),
            TextNode(" and another image ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "url_end"),
            TextNode(".", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_image_with_adjacent_images(self):
        old_nodes = [
            TextNode("This is a text node with adjacent images ![alt1](url1)![alt2](url2).", TextType.TEXT),
        ]

        new_nodes = split_nodes_image(old_nodes)

        expected_nodes = [
            TextNode("This is a text node with adjacent images ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "url1"),
            TextNode("alt2", TextType.IMAGE, "url2"),
            TextNode(".", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_link(self):
        old_nodes = [
            TextNode("This is a text node with a link [link text](link_url).", TextType.TEXT),
            TextNode("This is another text node.", TextType.TEXT),
        ]

        new_nodes = split_nodes_link(old_nodes)

        expected_nodes = [
            TextNode("This is a text node with a link ", TextType.TEXT),
            TextNode("link text", TextType.LINK, "link_url"),
            TextNode(".", TextType.TEXT),
            TextNode("This is another text node.", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_no_links(self):
        old_nodes = [
            TextNode("This is a text node without links.", TextType.TEXT),
            TextNode("This is another text node.", TextType.TEXT),
        ]

        new_nodes = split_nodes_link(old_nodes)

        expected_nodes = [
            TextNode("This is a text node without links.", TextType.TEXT),
            TextNode("This is another text node.", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)
        
    def test_split_nodes_link_with_multiple_links(self):
        old_nodes = [
            TextNode("This is a text node with multiple links [link1](url1) and [link2](url2).", TextType.TEXT),
        ]

        new_nodes = split_nodes_link(old_nodes)

        expected_nodes = [
            TextNode("This is a text node with multiple links ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(".", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_link_with_link_at_start_and_end(self):
        old_nodes = [
            TextNode("[start](url_start) This is a text node with a link [middle](url_middle) and another link [end](url_end).", TextType.TEXT),
        ]

        new_nodes = split_nodes_link(old_nodes)

        expected_nodes = [
            TextNode("start", TextType.LINK, "url_start"),
            TextNode(" This is a text node with a link ", TextType.TEXT),
            TextNode("middle", TextType.LINK, "url_middle"),
            TextNode(" and another link ", TextType.TEXT),
            TextNode("end", TextType.LINK, "url_end"),
            TextNode(".", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)
        
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

    def test_markdown_to_blocks_with_empty_lines(self):
        md = """
This is a paragraph with text.

```
This is a code block.
```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph with text.",
                "```\nThis is a code block.\n```",
            ],
        )
    
    def test_markdown_to_blocks_with_multiple_empty_lines(self):
        md = """
This is a paragraph with text.

```
This is a code block.
```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph with text.",
                "```\nThis is a code block.\n```",
            ],
        )

    def test_markdown_to_blocks_with_no_empty_lines(self):
        md = """This is a paragraph with text.

This is another paragraph with text.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph with text.",
                "This is another paragraph with text.",
            ],
        )
    def test_block_to_block_type_with_heading(self):
        result = block_to_block_type("# My heading")
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_not_heading_without_space(self):
        result = block_to_block_type("##Not a heading")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = """```
print("hello")
```"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = """> First quoted line
>Second quoted line"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = """- Apples
- Bread"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = """1. First item
2. Second item
3. Third item"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        result = block_to_block_type("A normal paragraph of text.")
        self.assertEqual(result, BlockType.PARAGRAPH)

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