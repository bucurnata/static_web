from textnode import TextType, TextNode
from htmlnode import HTMLNode

def main():
    test = TextNode("Hello", TextType.LINK, "https://example.com")
    print(test)
main()