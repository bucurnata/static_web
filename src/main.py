from textnode import TextType, TextNode
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode

def main():

    
    test = TextNode("Hello", TextType.LINK, "https://example.com")
    print(test)


main()
