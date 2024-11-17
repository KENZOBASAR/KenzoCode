# Main import
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.ttk import Treeview, Style
import tkinter.filedialog
from tkinter import messagebox, filedialog
from tkhtmlview import HTMLLabel
from pygments.lexers import HtmlLexer, PythonLexer, JavascriptLexer, JavaLexer, CssLexer, BatchLexer, CLexer, CppLexer, TextLexer, RustLexer, PowerShellLexer, PhpLexer, GoLexer, LuaLexer, BashLexer
from pygments.styles import get_style_by_name
from pygments import lex
import os
import subprocess
import time
from tkinterweb import HtmlFrame  # Import HtmlFrame to render web content

# Sample commands for each language
# This is a head pain!
LANGUAGE_COMMANDS = {
    "Python": {
        "def": "Define a function",
        "if": "If statement",
        "import": "Import module",
        "for": "Loops",
        "while": "Infinte Loops",
        "print": "Prints the string",
        "try": "Try to do",
    },
    "HTML": {
        "<div>": "Define a division",
        "<p>": "Define a paragraph",
        "<a>": "Define a link",
        "<marquee>": "Moving text or element",
        "<img>": "Image",
        "<style>": "Styling in CSS",
    },
    "JavaScript": {
        "function": "Define a function",
        "if": "If statement",
        "console": "Log output",
        "let": "Define a variable",
        "const": "Write a variable",
    },
    "Go": {
        "import": "Import",
        "package": "Package",
        "int": "Data int",
    },
    "PHP": {
        "echo": "Echos a string",
        "<?php": "Start of PHP",
        "array": "Array System",
        "filopen": "Opens a file",
    },
    "Java": {
        "public": "Public Void or element",
        "private": "Private Void or element",
        "import": "Import module or library",
        "void": "Function",
    },
    "CSS": {
        "body": "Body",
        "font-size": "Size of font",
        "background-color": "Background color of element in HTML",
        "color": "Foreground Color of element in HTML",
    },
    "C": {
        "#include": "Include/Declare Library",
        "//": "Comment",
        "int": "Point and if main entry point",
        "printf": "Prints a string",
        "scanf": "Take input",
    },
    "C++": {
        "if": "If Declare",
        "else": "If the user does not enter the right input",
        "cin": "Takes the input from the user",
        "cout": "Gives output",
        "endl": "End of line",
    },
    "BatchFile": {
        "echo": "Echos a string",
        "rem": "Comment",
        ":": "Label",
        "set": "Sets variable",
        "goto": "Goes to a label",
    },
    "Lua": {
        "local": "Variable",
        "if": "If statement",
        "else": "If user input is not equal to the answer or string",
        "while": "Loop",
        "for": "Loop",
    },
    "PowerShell": {
        "write-host": "Writes the string to screen",
        "exit": "Exits the application",
        "if": "If statement",
        "Function": "Declare function",
        "Cd": "Changes directory",
    },
    "Rust": {
        "let": "Declare variable",
        "bool": "Boolean",
        "fn": "Declare function",
        "println": "Prints a string",
        "struct": "Custom data type",
    },
    "Bash": {
        "echo": "Echos a string",
        "ls": "List files",
        "cd": "Change Directory",
        "touch": "Creates empty file",
        "rm": "Delete file",
    },
}
# fallback imports
try:
    from tkinter import *
    from tkinter import ttk
    import tkinter as tk
    from tkinter.ttk import Treeview, Style
    import tkinter.filedialog
    from tkinter import messagebox, filedialog
    from tkhtmlview import HTMLLabel
    from pygments.lexers import HtmlLexer, PythonLexer, JavascriptLexer, JavaLexer, CssLexer, BatchLexer, CLexer, CppLexer, RustLexer, PowerShellLexer, PhpLexer, GoLexer, LuaLexer, BashLexer
    from pygments.styles import get_style_by_name
    from pygments import lex
    import os
    import subprocess
    from tkinterweb import HtmlFrame  # Import HtmlFrame to render web content
except ImportError as e:
    print(f"Warning: {e} — Fallback imports in use.")

print("The code is not supposed to be on .PY use .PYW instead")
class CodeEditor(Tk):
    def __init__(self):
        super().__init__()

        # Initialize the language variable
        self.language = StringVar(value="Python")  # Default to Python

        # Window setup
        self.title("Untitled - Kenzo Code Editor")
        self.state("zoomed")  # Maximize the window
        self.geometry("1000x600")  # Increased width for sidebar
        self.configure(bg="#282c34")

        # Set up the Treeview style
        style = Style()
        style.configure("Custom.Treeview", background="#1e1e1e", foreground="#d4d4d4", fieldbackground="#1e1e1e")

        # Sidebar setup (for file navigation and ChatGPT)
        self.sidebar = Frame(self, width=150, bg="#282c34")  # Adjusted width for smaller sidebar
        self.sidebar.pack(side="left", fill="y")

        # Treeview setup for file navigation
        self.tree = Treeview(self.sidebar, selectmode="browse", show="tree", style="Custom.Treeview")
        self.tree.pack(expand=True, fill="both")

        # ChatGPT HTML rendering in sidebar
        self.chatgpt_frame = HtmlFrame(self.sidebar, width=150, height=600)  # Adjusted width for smaller frame
        self.chatgpt_frame.pack(side="left", fill="both", expand=True)

        # Text widget for code input
        self.text_area = Text(self, wrap="none", undo=True, bg="#1e1e1e", fg="#d4d4d4",
                              insertbackground="#ffffff", font=("Courier New", 12))
        self.text_area.pack(expand=True, fill="both")
        self.text_area.bind("<KeyRelease>", self.highlight_syntax)

        # Output widget for HTML rendering
        self.output_frame = Frame(self, bg="#282c34")
        self.output_label = HTMLLabel(self.output_frame, html="")
        self.output_label.pack(expand=True, fill="both")
        self.output_frame.pack(expand=True, fill="both", side="bottom")
        
        # Scrollbars
        self.scroll_x = Scrollbar(self, orient="horizontal", command=self.text_area.xview)
        self.scroll_y = Scrollbar(self, orient="vertical", command=self.text_area.yview)
        self.text_area.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.scroll_x.pack(side="bottom", fill="x")
        self.scroll_y.pack(side="right", fill="y")

        # Status bar setup
        self.status_bar = Label(self, text="Line: 1, Column: 1", bg="#282c34", fg="#d4d4d4", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

        # Create a right-click context menu
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="No suggestions", state="disabled")

        # Bind right-click to show context menu
        self.text_area.bind("<Button-3>", self.show_context_menu)

        # Menu
        self.create_menu()

        # Populate the Treeview with current directory contents
        self.populate_treeview(os.getcwd())

    def update_status(self, event=None):
        # Get the current position of the cursor (line, column)
        line, col = self.text_area.index(INSERT).split(".")
        self.status_bar.config(text=f"Line: {line}, Column: {col}")

        # Show the context menu
        self.context_menu.post(event.x_root, event.y_root)

    def show_context_menu(self, event):
        """Show context menu with commands based on the first typed character."""
        self.context_menu.delete(0, "end")  # Clear previous menu items
        current_line = self.text_area.get("insert linestart", "insert lineend")
        first_char = current_line.strip()[:1]  # Get first character

        # Get commands based on the current language and the first typed character
        commands = self.get_commands(first_char)

        # Add commands to the context menu
        for command, description in commands.items():
            self.context_menu.add_command(
                label=f"{command}: {description}",
                command=lambda cmd=command: self.insert_command(cmd)
            )

        # Show the context menu
        self.context_menu.post(event.x_root, event.y_root)

    def get_commands(self, first_char):
        """Get commands for the selected language that start with the given character."""
        language = self.language.get()
        commands = LANGUAGE_COMMANDS.get(language, {})
        filtered_commands = {cmd: desc for cmd, desc in commands.items() if cmd.startswith(first_char)}
        return filtered_commands

    def insert_command(self, command):
        """Insert the selected command at the current cursor position."""
        self.text_area.insert("insert", command)  # Insert command at the cursor position


    def create_menu(self):
        menu_bar = Menu(self)
        
        # File menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Render HTML", command=self.render_html)
        file_menu.add_command(label="Open in Command Prompt", command=self.open_in_command_prompt)  # New menu item
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Open Google", command=self.open_google)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Themes submenu under Edit
        themes_menu = Menu(edit_menu, tearoff=0)
        themes_menu.add_command(label="Light Theme", command=lambda: self.set_theme('light'))
        themes_menu.add_command(label="Dark Theme", command=lambda: self.set_theme('dark'))
        themes_menu.add_command(label="Solarized Dark", command=lambda: self.set_theme('solarized_dark'))
        themes_menu.add_command(label="Solarized Light", command=lambda: self.set_theme('solarized_light'))
        themes_menu.add_command(label="Solarized Blue", command=lambda: self.set_theme('solarized_blue'))
        themes_menu.add_command(label="Dark Blue", command=lambda: self.set_theme('dark_blue'))
        menu_bar.add_cascade(label="Themes", menu=themes_menu)


        # Language menu
        language_menu = Menu(menu_bar, tearoff=0)
        language_menu.add_radiobutton(label="Python", variable=self.language, value="Python")
        language_menu.add_radiobutton(label="HTML", variable=self.language, value="HTML")
        language_menu.add_radiobutton(label="JavaScript", variable=self.language, value="JavaScript")
        language_menu.add_radiobutton(label="Java", variable=self.language, value="Java")
        language_menu.add_radiobutton(label="CSS", variable=self.language, value="CSS")
        language_menu.add_radiobutton(label="BatchFile", variable=self.language, value="BatchFile")
        language_menu.add_radiobutton(label="C", variable=self.language, value="C")
        language_menu.add_radiobutton(label="C++", variable=self.language, value="C++")
        language_menu.add_radiobutton(label="Rust", variable=self.language, value="Rust")
        language_menu.add_radiobutton(label="PowerShell", variable=self.language, value="PowerShell")
        language_menu.add_radiobutton(label="PHP", variable=self.language, value="PHP")
        language_menu.add_radiobutton(label="Go", variable=self.language, value="Go")
        language_menu.add_radiobutton(label="Lua", variable=self.language, value="Lua")
        language_menu.add_radiobutton(label="Bash", variable=self.language, value="Bash")
        language_menu.add_radiobutton(label="Plain Text", variable=self.language, value="PlainText")
        menu_bar.add_cascade(label="Language", menu=language_menu)

        self.config(menu=menu_bar)

        # Language Templates menu
        templates_menu = Menu(menu_bar, tearoff=0)
        templates_menu.add_command(label="Insert Hello World", command=self.insert_hello_world)
        menu_bar.add_cascade(label="Language Templates", menu=templates_menu)

        self.config(menu=menu_bar)

        # Help menu (for About)
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.about_window)  # New About menu item
        help_menu.add_command(label="Credits", command=self.credits_window)  # New Credits menu item
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

    def set_theme(self, theme):
        """Apply the selected theme to the text area."""
        if theme == 'light':
            self.text_area.config(bg="#ffffff", fg="#000000", insertbackground="#000000")
        elif theme == 'dark':
            self.text_area.config(bg="#1e1e1e", fg="#d4d4d4", insertbackground="#ffffff")
        elif theme == 'solarized_dark':
            self.text_area.config(bg="#002b36", fg="#839496", insertbackground="#839496")
        elif theme == 'solarized_light':
            self.text_area.config(bg="#fdf6e3", fg="#657b83", insertbackground="#657b83")
        elif theme == 'solarized_blue':
            self.text_area.config(bg="#7D7AE1", fg="#010005", insertbackground="#7D7AE1")
        elif theme == 'dark_blue':
            self.text_area.config(bg="#001067", fg="#010005", insertbackground="#001067")
        else:
            print("Unknown theme:", theme)

    def credits_window(self):
        # Create a new Toplevel window for Credit
        credit_win = Toplevel(self)
        credit_win.title("Credits")
        credit_win.geometry("400x300")
        credit_win.configure(bg="#282c34")

        # Credit content
        credit_label = Label(credit_win, text="Kenzo Code Editor v1.3\n\nDeveloper: Kenzo Basar\n\nBeta Tester: Bigam Ligo \n\nDesigner: Bigam Ligo\n\nIdeas: Keni Basar\n\nVersion: 1.3", 
                            fg="#d4d4d4", bg="#C21213", font=("Courier New", 14), justify="center")
        credit_label.pack(expand=True)

        # Close button
        close_button = Button(credit_win, text="Close", command=credit_win.destroy, bg="#1e1e1e", fg="#d4d4d4", font=("Courier New", 12))
        close_button.pack(pady=10)

    def about_window(self):
        # Create a new Toplevel window for About
        about_win = Toplevel(self)
        about_win.title("About KenzoCode Editor")
        about_win.geometry("400x300")
        about_win.configure(bg="#282c34")

        # About content
        about_label = Label(about_win, text="Kenzo Code Editor v1.3\n\nDeveloped by KCR\n\nA simple yet powerful code editor\n\nVersion: 1.3", 
                            fg="#d4d4d4", bg="#282c34", font=("Courier New", 14), justify="center")
        about_label.pack(expand=True)

        # Close button
        close_button = Button(about_win, text="Close", command=about_win.destroy, bg="#1e1e1e", fg="#d4d4d4", font=("Courier New", 12))
        close_button.pack(pady=10)

    def open_google(self):
        # Open google website in the sidebar frame
        self.chatgpt_frame.load_url("https://google.com/")

    def open_in_command_prompt(self):
        current_directory = os.getcwd()  # Get the current working directory
        subprocess.Popen(['start', 'cmd.exe', '/K', f'cd {current_directory}'], shell=True)  # Use 'start' to open in a new window

    def create_new_tab(self):
        tab_frame = Frame(self.notebook, bg="#282c34")
        text_area = Text(tab_frame, wrap="none", undo=True, bg="#1e1e1e", fg="#d4d4d4", insertbackground="#ffffff", font=("Courier New", 12))
        text_area.pack(expand=True, fill="both")
        text_area.bind("<KeyRelease>", self.highlight_syntax)

        self.notebook.add(tab_frame, text="Untitled")

        # Store the text_area reference for later use
        self.text_area = text_area


    def new_file(self):
        self.create_new_tab()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.text_area.delete("1.0", END)
            self.text_area.insert("1.0", content)
            self.highlight_syntax()
            self.title(f"{file_path} - Code Editor")

    def save_file(self):
        if self.title().startswith("Untitled"):
            self.save_as_file()
        else:
            file_path = self.title().split(" - ")[0]
            self.write_to_file(file_path)

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.write_to_file(file_path)
            self.title(f"{file_path} - Code Editor")

    def write_to_file(self, file_path):
        try:
            with open(file_path, "w") as file:
                file.write(self.text_area.get("1.0", END))
            messagebox.showinfo("Save", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def highlight_syntax(self, event=None):
        code = self.text_area.get("1.0", END)
        for tag in self.text_area.tag_names():
            self.text_area.tag_delete(tag)
        
        # Select lexer based on the language
        lexer = None
        if self.language.get() == "Python":
            lexer = PythonLexer()
        elif self.language.get() == "HTML":
            lexer = HtmlLexer()
        elif self.language.get() == "JavaScript":
            lexer = JavascriptLexer()
        elif self.language.get() == "Java":
            lexer = JavaLexer()
        elif self.language.get() == "CSS":
            lexer = CssLexer()
        elif self.language.get() == "BatchFile":
            lexer = BatchLexer()
        elif self.language.get() == "C":
            lexer = CLexer()
        elif self.language.get() == "C++":
            lexer = CppLexer()
        elif self.language.get() == "Rust":
            lexer = RustLexer()
        elif self.language.get() == "PowerShell":
            lexer = PowerShellLexer()
        elif self.language.get() == "PHP":
            lexer = PhpLexer()
        elif self.language.get() == "Go":
            lexer = GoLexer()
        elif self.language.get() == "Lua":
            lexer = LuaLexer()
        elif self.language.get() == "Bash":
            lexer = BashLexer()
        elif self.language.get() == "PlainText":
            lexer = TextLexer()
        else:
            lexer = TextLexer()  # Default to plain text

        tokens = lex(code, lexer)
        style = get_style_by_name("monokai")
        
        for token, content in tokens:
            color = style.style_for_token(token).get("color", "#d4d4d4")
            tag = str(token)
            if content.strip():
                self.text_area.tag_configure(tag, foreground=f"#{color}")
                start = "1.0"
                while True:
                    start = self.text_area.search(content, start, stopindex=END)
                    if not start:
                        break
                    end = f"{start}+{len(content)}c"
                    self.text_area.tag_add(tag, start, end)
                    start = end

    def get_color_for_token(self, token):
        if token in ['Keyword', 'Name']:
            return "blue"
        elif token in ['String']:
            return "green"
        elif token in ['Comment']:
            return "gray"
        else:
            return "white"

    def render_html(self):
        html_code = self.text_area.get("1.0", END)
        self.output_label.set_html(html_code)
        self.output_frame.tkraise()

    def populate_treeview(self, directory):
        # Get the list of files and directories
        files = os.listdir(directory)

        # Create the root item for the Treeview
        root = self.tree.insert("", "end", text=directory, open=True)

        for file in files:
            full_path = os.path.join(directory, file)
            if os.path.isdir(full_path):
                self.tree.insert(root, "end", text=file, open=False)
            else:
                self.tree.insert(root, "end", text=file)

        # Bind keys for auto-pairing
        self.text_area.bind("<KeyRelease-[>", self.insert_pair)
        self.text_area.bind("<KeyRelease-{>", self.insert_pair)
        self.text_area.bind("<KeyRelease-(>", self.insert_pair)
        self.text_area.bind("<KeyRelease-\">", self.insert_pair)
        self.text_area.bind("<KeyRelease-\'>", self.insert_pair)
        self.text_area.bind("<KeyRelease-<>", self.insert_pair)

    def insert_hello_world(self):
        """Insert a Hello World template based on the selected language."""
        hello_world_code = {
            "Python": 'print("Hello, World!")',
            "HTML": '<!DOCTYPE html>\n<html>\n<head>\n    <title>Hello World</title>\n</head>\n<body>\n    <h1>Hello, World!</h1>\n</body>\n</html>',
            "JavaScript": 'console.log("Hello, World!");',
            "Java": 'public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
            "CSS": 'body {\n    font-family: Arial, sans-serif;\n    background-color: #f4f4f4;\n}\n\nh1 {\n    color: #333;\n}',
            "BatchFile": 'echo Hello, World!',
            "C": '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
            "C++": '#include <iostream>\n\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}',
            "Rust": 'fn main() {\n    println!("Hello, World!");\n}',
            "PowerShell": 'Write-Output "Hello, World!"',
            "PHP": '<?php\n echo "Hello, World!";\n?>',
            "Go": 'package main\nimport "fmt"\n \nfunc main() {\n    fmt.Println("Hello, World!")\n}',
            "Lua": '-- This is a comment\nprint("Hello, World!")',
            "Bash": '#!/bin/bash\necho "Hello, World!"',
            "PlainText": 'Hello, World!',
        }
        code = hello_world_code.get(self.language.get(), "Hello, World!")
        self.text_area.delete(1.0, END)
        self.text_area.insert(INSERT, code)

    def insert_pair(self, event):
        char_pairs = {
            "[": "]",
            "{": "}",
            "(": ")",
            "\"": "\"",
            "\'": "\'",
            "<": ">"
        }
        
        # Get the character typed
        char = event.char

        # Check if the typed character is in the pairing dictionary
        if char in char_pairs:
            # Insert the closing character immediately after the typed one
            self.text_area.insert("insert", char_pairs[char])
            # Move the cursor back by one to place it between the pair
            self.text_area.mark_set("insert", f"insert-1c")

        # Return "break" to prevent the default behavior (if needed)
        return "break"

# Emergency functions
# Contains elements if the original is broken
    def insert_pairemergency(self, event):
        char_pairs = {
            "[": "]",
            "{": "}",
            "(": ")",
            "\"": "\"",
            "\'": "\'",
            "<": ">"
        }
        
        # Get the character typed
        char = event.char

        # Check if the typed character is in the pairing dictionary
        if char in char_pairs:
            # Insert the closing character immediately after the typed one
            self.text_area.insert("insert", char_pairs[char])
            # Move the cursor back by one to place it between the pair
            self.text_area.mark_set("insert", f"insert-1c")

        # Return "break" to prevent the default behavior (if needed)
        return "break"

    def highlight_syntaxemergency(self, event=None):
        code = self.text_area.get("1.0", END)
        for tag in self.text_area.tag_names():
            self.text_area.tag_delete(tag)
        
        # Select lexer based on the language
        lexer = None
        if self.language.get() == "Python":
            lexer = PythonLexer()
        elif self.language.get() == "HTML":
            lexer = HtmlLexer()
        elif self.language.get() == "JavaScript":
            lexer = JavascriptLexer()
        elif self.language.get() == "Java":
            lexer = JavaLexer()
        elif self.language.get() == "CSS":
            lexer = CssLexer()
        elif self.language.get() == "BatchFile":
            lexer = BatchLexer()
        elif self.language.get() == "C":
            lexer = CLexer()
        elif self.language.get() == "C++":
            lexer = CppLexer()
        elif self.language.get() == "Rust":
            lexer = RustLexer()
        elif self.language.get() == "PowerShell":
            lexer = PowerShellLexer()
        elif self.language.get() == "PlainText":
            lexer = TextLexer()
        else:
            lexer = TextLexer()  # Default to plain text

        tokens = lex(code, lexer)
        style = get_style_by_name("monokai")
        
        for token, content in tokens:
            color = style.style_for_token(token).get("color", "#d4d4d4")
            tag = str(token)
            if content.strip():
                self.text_area.tag_configure(tag, foreground=f"#{color}")
                start = "1.0"
                while True:
                    start = self.text_area.search(content, start, stopindex=END)
                    if not start:
                        break
                    end = f"{start}+{len(content)}c"
                    self.text_area.tag_add(tag, start, end)
                    start = end

    def get_color_for_tokenemergency(self, token):
        if token in ['Keyword', 'Name']:
            return "blue"
        elif token in ['String']:
            return "green"
        elif token in ['Comment']:
            return "gray"
        else:
            return "white"

# Created and made by KCR-SOFT
# Modification and constribution allowed
# ...But ask permission at kanubello0000@gmail.com


if __name__ == "__main__":
    app = CodeEditor()
    app.mainloop()
