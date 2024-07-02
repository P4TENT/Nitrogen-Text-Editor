import re

# Sample text
text = '''
import os
import sys
from collections import defaultdict
from typing import List  # import typing
""" A docstring with import
import something_inside_docstring
"""
'''

# Define the regex pattern to match import/from statements
# Ensure that 'import' or 'from' is not preceded by a double quote
IMPORT_PATTERN = re.compile(r'(?<!")\b(import|from)\s+(\w+)')
# Define the regex pattern to match comments
COMMENT_PATTERN = re.compile(r'(^|\s)#.*')

# Define the ANSI escape code for yellow
YELLOW = '\033[93m'
RESET = '\033[0m'

# Function to highlight the words after import/from
def highlight_imports(text):
    # Split the text into lines to handle each line individually
    lines = text.split('\n')
    highlighted_lines = []

    for line in lines:
        # Check if the line is a comment
        if COMMENT_PATTERN.search(line):
            highlighted_lines.append(line)
        else:
            # Replace import/from matches with highlighted version
            def replace_import(match):
                return f"{match.group(1)} {YELLOW}{match.group(2)}{RESET}"
            
            highlighted_line = IMPORT_PATTERN.sub(replace_import, line)
            highlighted_lines.append(highlighted_line)

    # Join the lines back into a single string
    return '\n'.join(highlighted_lines)

# Apply the highlighting
highlighted_text = highlight_imports(text)
print(highlighted_text)
