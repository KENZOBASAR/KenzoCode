from tkinter import *
from tkinter.ttk import Treeview, Style
import tkinter.filedialog
from tkinter import messagebox, filedialog
from tkhtmlview import HTMLLabel
from pygments.lexers import HtmlLexer, PythonLexer, JavascriptLexer, JavaLexer, CssLexer, TextLexer
from pygments.styles import get_style_by_name
from pygments import lex
import os
import subprocess
from tkinterweb import HtmlFrame  # Import HtmlFrame to render web content

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

        # Menu
        self.create_menu()

        # Populate the Treeview with current directory contents
        self.populate_treeview(os.getcwd())

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

        # Language menu
        language_menu = Menu(menu_bar, tearoff=0)
        language_menu.add_radiobutton(label="Python", variable=self.language, value="Python")
        language_menu.add_radiobutton(label="HTML", variable=self.language, value="HTML")
        language_menu.add_radiobutton(label="JavaScript", variable=self.language, value="JavaScript")
        language_menu.add_radiobutton(label="Java", variable=self.language, value="Java")
        language_menu.add_radiobutton(label="CSS", variable=self.language, value="CSS")
        menu_bar.add_cascade(label="Language", menu=language_menu)

        self.config(menu=menu_bar)

    def open_google(self):
        # Open google website in the sidebar frame
        self.chatgpt_frame.load_url("https://google.com/")

    def open_in_command_prompt(self):
        current_directory = os.getcwd()  # Get the current working directory
        subprocess.Popen(['start', 'cmd.exe', '/K', f'cd {current_directory}'], shell=True)  # Use 'start' to open in a new window

    def new_file(self):
        self.text_area.delete("1.0", END)
        self.title("Untitled - Code Editor")

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

if __name__ == "__main__":
    app = CodeEditor()
    app.mainloop()