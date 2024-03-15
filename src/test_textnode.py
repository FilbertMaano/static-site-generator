import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        node3 = TextNode("This is a text node", "italic")
        node4 = TextNode("This is a text node", "italic", "https://google.com")
        node5 = TextNode("This is a text node", "italic", "https://facebook.com")
        self.assertEqual(node, node)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node4, node5)
        self.assertEqual(node4, node4)


if __name__ == "__main__":
    unittest.main()
