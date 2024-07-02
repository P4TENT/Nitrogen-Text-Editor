import SHARED_STATE
import re
import customtkinter as ctk
text_area = SHARED_STATE.SHARED_text_area

KEYWORDS1 = ["def", "class", "import", "from", "with", "as", "lambda", "True", "False", "None", "is", "in", "global"]
KEYWORDS2 = ["if", "else", "elif", "return", "for", "while", "break", "continue", "try", "except", "finally"]
KEYWORD_PATTERN1 = re.compile(r'\b(?:' + '|'.join(KEYWORDS1) + r')\b')
KEYWORD_PATTERN2 = re.compile(r'\b(?:' + '|'.join(KEYWORDS2) + r')\b')
COMMENT_PATTERN = re.compile(r'(?<!")#.*')
FUNCTION_DEF_PATTERN = re.compile(r'(\w+)\s*\(')
FUNCTION_CALL_PATTERN = re.compile(r'\b(\w+)\s*\(')
NUMBER_PATTERN = re.compile(r'\b\d+(\.\d+)?\b')
UPPERCASE_WORD_PATTERN = re.compile(r'\b[A-Z][A-Z0-9_]+\b')
OPERATOR_PATTERN = re.compile(r'(\+|\-|\*|\/|\*\*|!=|==|<=|>=|<|>|=|\b)')
LOGICAL_OPERATOR_PATTERN = re.compile(r'\b(?:not|and|or|in|is|>|>=|<|<=|==|!=)\b')
TYPE_PATTERN = re.compile(r'\b(?:int|str|list|dict|set|tuple|float|complex|bool|None|True|False)\b')
DOCSTRING_PATTERN = re.compile(r'""".*?"""|\'\'\'.*?\'\'\'')
EXCEPTION_PATTERN = re.compile(r'\b(?:Exception|ValueError|TypeError|IndexError|KeyError|AttributeError|NameError|IOError|FileNotFoundError)\b' )
DECORATOR_PATTERN = re.compile(r'@\w+')
ARGUMENT_PATTERN = re.compile(r'\b(\w+)\b(?=\s*[,)]|\s*=)')
STRING_PATTERN = re.compile(r'(["\'])(?:(?=(\\?))\2.)*?\1')
YELLOW_ARGUMENT_PATTERN = re.compile(r'\b(import|from)\s+(\w+)')

def _setup_tags():
    # Define the One Dark Pro colors for syntax highlighting
    text_area.tag_config("yellow_argument", foreground="#E5C07B")  # Yellow for arguments
    text_area.tag_config("keyword1", foreground="#C678DD")  # Purple for keywords
    text_area.tag_config("keyword2", foreground="#C678DD")  # Purple for keywords
    text_area.tag_config("function", foreground="#61AFEF")  # Blue for functions
    text_area.tag_config("number", foreground="#D19A66")    # Orange for numbers
    text_area.tag_config("operator", foreground="#E0FFFF")   # Red for operators
    text_area.tag_config("logical", foreground="#C678DD")    # Purple for logical operators
    text_area.tag_config("type", foreground="#E5C07B")       # Yellow for types
    text_area.tag_config("docstring", foreground="#98C379")  # Green for docstrings
    text_area.tag_config("exception", foreground="#E06C75")  # Red for exceptions
    text_area.tag_config("decorator", foreground="#61AFEF")  # Blue for decorators
    text_area.tag_config("argument", foreground="#E06C75")   # Red for arguments
    text_area.tag_config("uppercase", foreground="#E5C07B")  # Red for uppercase words
    text_area.tag_config("string", foreground="#98C379")    # Green for strings
    text_area.tag_config("comment", foreground="#5C6370")   # Grey for comments

def _highlight_syntax(event=None):
    _setup_tags()
    # Get the current line number where the modification happened
    current_line = text_area.index("insert").split('.')[0]
    current_line = int(current_line)
    
    # Define the lines to be highlighted: the current line, one line before, and one line after
    start_line = max(current_line - 1, 1)  # Avoid going below line 1
    end_line = current_line + 3
    
    # Convert lines to text indexes
    start_index = f"{start_line}.0"
    end_index = f"{end_line}.end"
    
    # Remove previous tags from the specified lines
    text_area.tag_remove("all", start_index, end_index)
    
    # Get the text from the specified lines
    text = text_area.get(start_index, end_index)
    
    # Apply patterns to the specified lines
    _apply_pattern(FUNCTION_DEF_PATTERN, text, "function", group=1)  # Group 1 for function name in definitions
    _apply_pattern(FUNCTION_CALL_PATTERN, text, "function", group=1)  # Group 1 for function name in calls
    _apply_pattern(YELLOW_ARGUMENT_PATTERN, text, "yellow_argument")
    _apply_pattern(KEYWORD_PATTERN1, text, "keyword1")
    _apply_pattern(KEYWORD_PATTERN2, text, "keyword2")
    _apply_pattern(NUMBER_PATTERN, text, "number")  # Added for numbers
    _apply_pattern(OPERATOR_PATTERN, text, "operator")  
    _apply_pattern(LOGICAL_OPERATOR_PATTERN, text, "logical")
    _apply_pattern(TYPE_PATTERN, text, "type")
    _apply_pattern(DOCSTRING_PATTERN, text, "docstring")
    _apply_pattern(EXCEPTION_PATTERN, text, "exception")
    _apply_pattern(DECORATOR_PATTERN, text, "decorator")
    _apply_pattern(COMMENT_PATTERN, text, "comment")
    _apply_pattern(ARGUMENT_PATTERN, text, "argument")
    _apply_pattern(UPPERCASE_WORD_PATTERN, text, "uppercase")
    _apply_pattern(STRING_PATTERN, text, "string")
    
def _highlight_syntax_idle(event=None):
    _setup_tags()
    
    text_area.tag_remove("function", "1.0", "end-1c")
    text_area.tag_remove("yellow_argument", "1.0", "end-1c")
    text_area.tag_remove("keyword1", "1.0", "end-1c")
    text_area.tag_remove("keyword2", "1.0", "end-1c")
    text_area.tag_remove("number", "1.0", "end-1c")
    text_area.tag_remove("operator", "1.0", "end-1c")
    text_area.tag_remove("logical", "1.0", "end-1c")
    text_area.tag_remove("type", "1.0", "end-1c")
    text_area.tag_remove("docstring", "1.0", "end-1c")
    text_area.tag_remove("exception", "1.0", "end-1c")
    text_area.tag_remove("decorator", "1.0", "end-1c")
    text_area.tag_remove("comment", "1.0", "end-1c")
    text_area.tag_remove("argument", "1.0", "end-1c")
    text_area.tag_remove("uppercase", "1.0", "end-1c")
    text_area.tag_remove("string", "1.0", "end-1c")
    
    line_count = int(text_area.index('end-1c').split('.')[0])
    
    for line in range(1, line_count + 1):
        line_start = f"{line}.0"
        line_end = f"{line}.end"
        text = text_area.get(line_start, line_end)
        
        _apply_pattern_idle(FUNCTION_DEF_PATTERN, text, "function", line_start, group=1)
        _apply_pattern_idle(FUNCTION_CALL_PATTERN, text, "function", line_start, group=1)
        _apply_pattern_idle(YELLOW_ARGUMENT_PATTERN, text, "yellow_argument", line_start)
        _apply_pattern_idle(KEYWORD_PATTERN1, text, "keyword1", line_start)
        _apply_pattern_idle(KEYWORD_PATTERN2, text, "keyword2", line_start)
        _apply_pattern_idle(NUMBER_PATTERN, text, "number", line_start) 
        _apply_pattern_idle(OPERATOR_PATTERN, text, "operator", line_start)  
        _apply_pattern_idle(LOGICAL_OPERATOR_PATTERN, text, "logical", line_start)
        _apply_pattern_idle(TYPE_PATTERN, text, "type", line_start)
        _apply_pattern_idle(DOCSTRING_PATTERN, text, "docstring", line_start)
        _apply_pattern_idle(EXCEPTION_PATTERN, text, "exception", line_start)
        _apply_pattern_idle(DECORATOR_PATTERN, text, "decorator", line_start)
        _apply_pattern_idle(COMMENT_PATTERN, text, "comment", line_start)
        _apply_pattern_idle(ARGUMENT_PATTERN, text, "argument", line_start)
        _apply_pattern_idle(UPPERCASE_WORD_PATTERN, text, "uppercase", line_start)
        _apply_pattern_idle(STRING_PATTERN, text, "string", line_start)

def _apply_pattern_idle(pattern, text, tag, line_start, group=None):
    for match in re.finditer(pattern, text):
        start_index = f"{line_start}+{match.start()}c"
        end_index = f"{line_start}+{match.end()}c"
        if group is not None:
            end_index = f"{line_start}+{match.start(group) + len(match.group(group))}c"
        text_area.tag_add(tag, start_index, end_index)

def _apply_pattern(pattern, text, tag, group=None):
    _setup_tags()
    current_line = text_area.index("insert").split('.')[0]
    current_line = int(current_line)
    start_line = max(current_line - 1, 1)
    start_index = f"{start_line}.0"
    pos = 0
    for match in re.finditer(pattern, text):
        start_offset = match.start()
        end_offset = match.end()
        start_idx = f"{start_index}+{start_offset}c"
        end_idx = f"{start_index}+{end_offset}c"
        text_area.tag_add(tag, start_idx, end_idx)

# Function to get the current line number of the cursor
def _get_cursor_line_number(textbox):
    index = textbox.index(ctk.INSERT)  # Get the cursor position as 'line.column'
    line_number, _ = map(int, index.split('.'))  # Split the index to get the line number
    return line_number

# Function to update the background color of the entire line where the cursor is
def _update_line_background(textbox, color):
    # Remove previous line background tag if it exists
    textbox.tag_remove('highlight_line', '1.0', ctk.END)
    
    # Get the line number where the cursor is
    line_number = _get_cursor_line_number(textbox)
    
    # Define the background color for the entire line
    start_index = f'{line_number}.0'
    end_index = f'{line_number}.end+1c'  # Extend to cover the entire line including the space after the last character
    textbox.tag_add('highlight_line', start_index, end_index)
    textbox.tag_config('highlight_line', background=color)

# Function to clear the background of the highlighted line
def _clear_line_background(textbox):
    textbox.tag_remove('highlight_line', '1.0', ctk.END)

# Example function to be called on cursor movement
def _highlight_cursor_line(event):
    _clear_line_background(text_area)  # Clear the previous line background
    _update_line_background(text_area, '#34424c')       
    
def _change_tabs(value):
    SHARED_STATE.SHARED_ChangeTabs(value)
    _highlight_syntax_idle()

def EXT_NITRO_SYNTAX():
    _highlight_syntax_idle()
    text_area.bind("<KeyPress>", _highlight_syntax) 
    text_area.bind("<Motion>", _highlight_syntax) 
    text_area.bind("<Motion>", _highlight_cursor_line) 
    text_area.bind('<ButtonRelease-1>', _highlight_cursor_line)
    text_area.bind('<KeyRelease>', _highlight_cursor_line)
    SHARED_STATE.SHARED_text_tabs1.configure(command=lambda value: _change_tabs(value))
    SHARED_STATE.SHARED_text_tabs2.configure(command=lambda value: _change_tabs(value))
