import unittest

from textnode import TextNode, TextType
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_link, text_to_textnodes

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_images_no_result(self):
        text = "This text has no images."
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_links_no_result(self):
        text = "This text has no links."
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_links_ignores_images(self):
        text = "This is a link [link](url.com) and this is an image ![image](img.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "url.com")], matches)

    def test_extract_images_ignores_links(self):
        text = "This is a link [link](url.com) and this is an image ![image](img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "img.png")], matches)

    def test_empty_alt_text_and_url(self):
        text_img = "Here is an image with no alt: ![](https://img.com/a.png)"
        text_link = "Here is a link with no url: [click me]()"
        
        self.assertListEqual([("", "https://img.com/a.png")], extract_markdown_images(text_img))
        self.assertListEqual([("click me", "")], extract_markdown_links(text_link))

##########################################################################################

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_image_text_with_image_first(self):
        node = TextNode(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
            ],
            new_nodes,
        )
    
    def test_no_images_in_text(self):
        node = TextNode("This is a text with no images", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is a text with no images", TextType.TEXT)], new_nodes)

    def test_images_ignores_links(self):
        node = TextNode("This is a link [link](url.com) and this is an image ![image](img.png)", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is a link [link](url.com) and this is an image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img.png")
            ],
            new_nodes,
        )

##########################################################################################

    def test_split_link_text(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ], 
            new_nodes,
        )

        def test_no_images_in_text(self):
            node = TextNode("This is a text with no links", TextType.TEXT)
            new_nodes = split_nodes_link([node])
            self.assertListEqual([TextNode("This is a text with no links", TextType.TEXT)], new_nodes)

    def test_links_ignores_images(self):
        node = TextNode("This is a link [link](url.com) and this is an image ![image](img.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a link ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
                TextNode(" and this is an image ![image](img.png)", TextType.TEXT),
            ],
            new_nodes,
        )
        

##########################################################################################

    def test_complete_split(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_node
        )
        
    def test_complete_split_no_bold(self):
        text = "This is text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_node
        )
    def test_complete_split_no_image(self):
        text = "This is text with an _italic_ word and a `code block` and a [link](https://boot.dev)"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_node
        )
    def test_with_nothing(self):
        text = "This is text"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text", TextType.TEXT),
            ],
            new_node
        )

if __name__ == "__main__":
    unittest.main()