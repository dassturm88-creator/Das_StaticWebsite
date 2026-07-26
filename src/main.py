from textnode import TextNode, TextType
from copystatic import delete_public, create_public, copy_static
from gencontent import generate_pages_recursive
import os
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)
    
    delete_public()
    create_public()
    copy_static("static", "public")

    generate_pages_recursive("content", "template.html", "public", basepath)

main()