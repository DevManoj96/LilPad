import tkinter as tk
from tkinter import messagebox, filedialog, font, simpledialog
import pyperclip
import webbrowser


default_font = ("Segoe UI", 12)

class LilPad:
    def __init__(self, root):
        root.option_add("*Font", default_font)
        self.root = root
        self.root.title("LilPad")
        self.root.geometry('800x600')
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        self.current_font = font.Font(family="Segoe UI", size=12)

        # File Menu Entries
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file, font=default_font)
        self.file_menu.add_command(label="Open", command=self.open_file, font=default_font)
        self.file_menu.add_command(label="Save", command=self.save_file, font=default_font)
        self.file_menu.add_command(label="Save As", command=self.save_as_file, font=default_font)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit, font=default_font)

        # Edit Menu Entries
        self.edit_menu = tk.Menu(self.root, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.undo_text, font=default_font)
        self.edit_menu.add_command(label="Redo", command=self.redo_text, font=default_font)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_text, font=default_font)
        self.edit_menu.add_command(label="Copy", command=self.copy_text, font=default_font)
        self.edit_menu.add_command(label="Paste", command=self.paste_text, font=default_font)
        self.edit_menu.add_command(label="Delete", command=self.delete_selection, font=default_font)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", command=self.find_text, font=default_font)
        self.edit_menu.add_command(label="Replace", command=self.replace_text, font=default_font)
        self.edit_menu.add_command(label="Select All", command=lambda: self.text_area.tag_add("sel", "1.0", "end"), font=default_font)

        # Format Menu Entries
        self.format_menu = tk.Menu(self.root, tearoff=0)
        self.format_menu.add_command(label="Zoom In", command=self.zoom_in, font=default_font)
        self.format_menu.add_command(label="Zoom Out", command=self.zoom_out, font=default_font)
        self.format_menu.add_separator()
        self.format_menu.add_command(label="Toggle Theme", command=self.toggle_theme, font=default_font)
        self.format_menu.add_command(label="Font", command=self.choose_font, font=default_font)
        self.font_menu = tk.Menu(self.format_menu, tearoff=0)
        self.format_menu.add_cascade(label="Select Font", menu=self.font_menu, font=default_font)

        # Help Menu Entries
        self.help_menu = tk.Menu(self.root, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about, font=default_font)
        self.help_menu.add_command(label="Docs", command=self.show_docs, font=default_font)
        self.help_menu.add_command(label="Shortcuts", command=self.show_shortcuts, font=default_font)

        # Main Menubar
        self.menubar.add_cascade(label="File", menu=self.file_menu, font=default_font)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu, font=default_font)
        self.menubar.add_cascade(label="Format", menu=self.format_menu, font=default_font)
        self.menubar.add_cascade(label="Help", menu=self.help_menu, font=default_font)

        # Text Area
        self.text_area = tk.Text(self.root, undo=True, wrap='word', font=self.current_font)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        self.current_file_path = None
        self.fonts = font.families()    # Listing all fonts

        # Add all the fonts to fontmenu
        for font_name in self.fonts:
            self.font_menu.add_command(label=font_name, command=lambda f=font_name: self.set_font(f), font=default_font)
        
        # Default dark mode configuration
        self.is_dark = False

        # Autosaving file after 30 seconds
        self.root.after(30000, lambda: self.autosave())

        # Bindings
        self.root.bind("<Control-n>", lambda _: self.new_file())
        self.root.bind("<Control-o>", lambda _: self.open_file())
        self.root.bind("<Control-s>", lambda _: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda _: self.save_as_file())
        self.root.bind("<Control-q>", lambda _: self.root.quit())
        self.root.bind("<Control-z>", lambda _: self.undo_text())
        self.text_area.unbind("<Control-y>")
        self.root.bind("<Control-y>", lambda _: self.redo_text())
        self.root.bind("<Control-x>", lambda _: self.cut_text())
        self.root.bind("<Control-c>", lambda _: self.copy_text())
        self.root.bind("<Delete>", lambda _: self.delete_selection())
        self.root.bind("<Control-a>", lambda _: self.text_area.tag_add("sel", "1.0", "end"))
        self.root.bind("<Control-f>", lambda _: self.find_text())
        self.root.bind("<Control-h>", lambda _: self.replace_text())
        self.root.bind("<Control-w>", lambda _: self.word_count())
        self.root.bind("<Control-equal>", lambda _: self.zoom_in())
        self.root.bind("<Control-minus>", lambda _: self.zoom_out())
        self.root.bind("<Control-d>", lambda _: self.toggle_theme())
        self.root.bind("<Control-u>", lambda _: self.toggle_underline())


    def new_file(self):
        self.current_file_path = None
        self.text_area.delete(1.0, tk.END)
        self.root.title("Untitled 1 - LilPad")

    def open_file(self):
        file = filedialog.askopenfilename()
        if file:
            with open(file, "r") as f:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, f.read())
            self.current_file_path = file 
            self.root.title(f"{file} - LilPad")

    def save_file(self):
        if self.current_file_path:
            with open(self.current_file_path, "w") as f:
                f.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", ".txt"), ("All Files", "*.*")])

        if file_path:
            with open(file_path, "w") as f:
                f.write(self.text_area.get(1.0, tk.END))

            self.current_file_path = file_path
            self.root.title(f"{file_path} - LilPad")

    def cut_text(self):
        try:
            content = self.text_area.selection_get()
            pyperclip.copy(content) # Copying the selected text
            
            self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST) # Delete the text starting from index 1st to the last index of selected text
        except tk.TclError:
            pass

    def copy_text(self):
        try:
            content = self.text_area.selection_get()
            pyperclip.copy(content)
        except tk.TclError:
            pass

    def paste_text(self):
        text = pyperclip.paste()
        try:
            self.text_area.insert(tk.END, text)
        except tk.TclError:
            pass

    def delete_selection(self):
        self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)       

    def find_text(self):
        find_txt = simpledialog.askstring("Find", "Enter text to find:", parent=self.root)
        self.text_area.tag_remove('found', '1.0', tk.END)
        if find_txt:
            start_index = self.text_area.search(find_txt, "1.0", stopindex="end")
            if start_index:
                end_index = f"{start_index}+{len(find_txt)}c"
                self.text_area.tag_add('found', start_index, end_index)
        
            self.text_area.tag_config('found', foreground='white', background='blue')

        self.root.after(15000, lambda: self.text_area.tag_delete('found')) # Remove the blue highlight after 15 seconds

    def replace_text(self):
        find_str = simpledialog.askstring("Find and Replace", "Enter the text to find:", parent=self.root)
        replace_str = simpledialog.askstring("Find and Replace", "Enter the text to replace:", parent=self.root)

        if find_str and replace_str:
            content = self.text_area.get(1.0, tk.END)
            replaced_content = content.replace(find_str, replace_str)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, replaced_content)

    def word_count(self):
        content = self.text_area.get(1.0, tk.END)
        word_count = len(content.split())
        char_count = len(content)
        messagebox.showinfo("Word Count", f"Words: {word_count}\nCharacters: {char_count}")

    def set_font(self, font_name):
        new_font = font.Font(family=font_name, size=12)
        self.text_area.config(font=new_font)

    def choose_font(self):
        font_name = simpledialog.askstring("Font", "Enter font family (e.g., Arial):", parent=self.root)
        font_size = simpledialog.askinteger("Font Size", "Enter font size:", parent=self.root)
        if font_name and font_size:
            new_font = font.Font(family=font_name, size=font_size)
            self.text_area.config(font=new_font)

    def zoom_in(self):
        new_size = self.current_font.actual("size") + 2 # Increasing the font by 2
        self.current_font.configure(size=new_size)

    def zoom_out(self):
        new_size = self.current_font.actual("size") - 2 # Decreasing the font by 2
        if new_size > 6:    # Ensuring the font not go small than 6 size
            self.current_font.configure(size=new_size)
    
    def toggle_underline(self):
        try:
            current_tags = self.text_area.tag_names(tk.SEL_FIRST)
            if "underline" in current_tags:
                self.text_area.tag_remove("underline", tk.SEL_FIRST, tk.SEL_LAST)   # If underline already exists then remove it
            else:
                underline_font = font.Font(self.text_area, self.text_area.cget("font"))
                underline_font.configure(underline=True) # Enabling underline in current font
                self.text_area.tag_configure("underline", font=underline_font)
                self.text_area.tag_add("underline", tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass
    
    def undo_text(self):
        self.text_area.edit_undo()

    def redo_text(self):
        self.text_area.edit_redo()

    def toggle_theme(self):
        dark_theme = {
            "background": "#222831",       # dark gray-blue
            "foreground": "#EEEEEE",       # soft white
            "insertbackground": "#00ADB5", # teal caret
            "txt_background": "#393E46",   # editor background
            "txt_foreground": "#FFFFFF",   # text color
            "highlight": "#58A6FF",      # semi-transparent teal selection
            "status": "#222831"            # status bar
        }

        light_theme = {
            "background": "#F8F9FA",       # light gray
            "foreground": "#212529",       # dark text
            "insertbackground": "#0D6EFD", # blue caret
            "txt_background": "#FFFFFF",   # editor background
            "txt_foreground": "#212529",   # text color
            "highlight": "#58A6FF",        # light blue selection
            "status": "#E9ECEF"            # status bar
        }

        self.is_dark = not self.is_dark
        theme = dark_theme if self.is_dark else light_theme

        # Configure theme for all the menubars
        self.menubar.config(fg=theme["foreground"], bg=theme["background"], activebackground=theme["highlight"])
        self.file_menu.config(fg=theme["foreground"], bg=theme["background"], activebackground=theme["highlight"])
        self.edit_menu.config(fg=theme["foreground"], bg=theme["background"], activebackground=theme["highlight"])
        self.format_menu.config(fg=theme["foreground"], bg=theme["background"], activebackground=theme["highlight"])
        self.help_menu.config(fg=theme["foreground"], bg=theme["background"], activebackground=theme["highlight"])

        # Configure theme for text widget
        self.text_area.config(
            fg=theme["txt_foreground"],
            bg=theme["txt_background"],
            insertbackground=theme["insertbackground"],
            selectbackground=theme["highlight"]
        )

    def autosave(self):
        if self.current_file_path:
            try:
                with open(self.current_file_path, "w") as f:
                    f.write(self.text_area.get(1.0, tk.END))
            except Exception:
                pass

    def show_about(self):
        messagebox.showinfo(
            "About",
            "LilPad Version 1.0\n\n"
            "LilPad is a lightweight text editor made with python. Its main goal to give people a great, light and open source editor\n"
            "Free feel to help me improve it.\n"
            "For more information, Check out my github."
        )

    def show_docs(self):
        try:
            webbrowser.open_new_tab("https://github.com/DevManoj96/LilPad/blob/main/DOCUMENTATIONS.md")
        except webbrowser.Error as e:
            messagebox.showerror("Error", str(e))

    def show_shortcuts(self):
        shortcuts = (
            "File Operations:\n"
            "  Ctrl+N: New File\n"
            "  Ctrl+O: Open File\n"
            "  Ctrl+S: Save File\n"
            "  Ctrl+Shift+S: Save As\n"
            "  Ctrl+Q: Quit\n\n"
            "Edit Operations:\n"
            "  Ctrl+Z: Undo\n"
            "  Ctrl+Y: Redo\n"
            "  Ctrl+X: Cut\n"
            "  Ctrl+C: Copy\n"
            "  Ctrl+V: Paste\n"
            "  Delete: Delete Selection\n"
            "  Ctrl+A: Select All\n\n"
            "Search and Replace:\n"
            "  Ctrl+F: Find\n"
            "  Ctrl+H: Replace\n\n"
            "View Operations:\n"
            "  Ctrl+W: Word Count\n"
            "  Ctrl+=: Zoom In\n"
            "  Ctrl+-: Zoom Out\n"
            "  Ctrl+D: Toggle Theme\n"
            "  Ctrl+U: Toggle Underline\n\n"
        )
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)

if __name__ == '__main__':
    root = tk.Tk()
    app = LilPad(root)
    root.mainloop()
