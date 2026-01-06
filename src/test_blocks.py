import unittest

from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType
'''
class TestBlockMarkdown(unittest.TestCase):
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
    def test_markdown_to_blocks_newlines(self):
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

    def test_markdown_to_blocks_empty(self):
        # Should return an empty list if there are no blocks
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
        
    def test_markdown_to_blocks_whitespace(self):
        md = """
    This block has leading whitespace    

    This block has trailing whitespace    
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This block has leading whitespace",
                "This block has trailing whitespace",
            ],
        )
'''

############################################################################################
"""
class TestBlockTypes(unittest.TestCase):
    # --- HEADING TESTS ---
    def test_block_to_block_type_headings_valid(self):
        # Test case 1: Single hash
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        
        # Test case 2: Double hash
        block = "## This is a sub-heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_headings_complex(self):
        # Test case 3: Six hashes (max level)
        block = "###### This is a small heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        
        # Test case 4: Invalid heading (no space after hash) - Should fallback to PARAGRAPH
        block = "#Invalid heading" 
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- CODE BLOCK TESTS ---
    def test_block_to_block_type_code_valid(self):
        # Test case 1: Valid start and end backticks
        block = "```\ndef x():\n    pass\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_invalid(self):
        # Test case 2: Missing closing backticks - Should fallback to PARAGRAPH
        block = "```\nThis is code without closing ticks"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- QUOTE TESTS ---
    def test_block_to_block_type_quote_valid(self):
        # Test case 1: All lines start with >
        block = "> This is a quote\n> This is line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_invalid(self):
        # Test case 2: Middle line missing > - Should fallback to PARAGRAPH
        block = "> This is a quote\nThis line is missing the char\n> Back to quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- ORDERED LIST TESTS (Bonus based on your code logic) ---
    def test_block_to_block_type_ordered_valid(self):
        # Valid incrementing list
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LISTS)

    def test_block_to_block_type_ordered_invalid_order(self):
        # Invalid sequence (1 then 3) - Should fallback to PARAGRAPH
        block = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
"""

if __name__ == "__main__":
    unittest.main()