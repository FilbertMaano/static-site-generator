import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node1 = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        html_node2 = HTMLNode()
        self.assertEqual(html_node2.props_to_html(), None)
        self.assertEqual(
            html_node1.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )


if __name__ == "__main__":
    unittest.main()
