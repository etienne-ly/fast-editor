from tkinter import *
import re

# defining constants
BGCOLOR = "#282C34"
STATUSCOLOR = "#22272e"
TEXTCOLOR = "#ABB2BF"
KEYWORDCOLOR = "#C678DD"
STRINGCOLOR = "#98C379"
INTCOLOR = "#E5C07B"
FUNCCOLOR = "#61AFEF"
FIRACODE = ("Consolas", 12)

# initializing the tk window as root
root = Tk()

# window configuration
root.rowconfigure(0, weight=5)
root.columnconfigure(0, weight=1)
root.title("fast editor")

# function to check syntax
def check_syntax(*args):
    get_cursor_position()
    lines = editor.get("1.0", END).split("\n")
    line = 0
    for code in lines:
        line += 1
        
        # search for keywords
        expression = r'\b(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b'
        matches = re.finditer(expression, code)
        for match in matches:
            editor.tag_add("keyword", f"{line}.{match.start()}", f"{line}.{match.end()}")
            
        # search for strings
        expression = r'\".+?\"'
        matches = re.finditer(expression, code)
        for match in matches:
            editor.tag_add("string", f"{line}.{match.start()}", f"{line}.{match.end()}")
            
        # search for ints
        expression = r'\d+'
        matches = re.finditer(expression, code)
        for match in matches:
            editor.tag_add("int", f"{line}.{match.start()}", f"{line}.{match.end()}")
            
        # search for functions
        expression = r'\S+(?=\()'
        matches = re.finditer(expression, code)
        for match in matches:
            editor.tag_add("func", f"{line}.{match.start()}", f"{line}.{match.end()}")
            
def get_cursor_position(*args):
    curr_char = editor.index(INSERT).split(".")
    char_lbl.config(text=f"line {curr_char[0]} : char {curr_char[1]}")

# main frame containing the text editor
main_frame = Frame(root, bg=BGCOLOR)
editor = Text(main_frame, bg=BGCOLOR, fg=TEXTCOLOR, font=FIRACODE, highlightthickness=0, relief=FLAT, insertbackground=TEXTCOLOR)
editor.tag_config("keyword", foreground=KEYWORDCOLOR)
editor.tag_config("string", foreground=STRINGCOLOR)
editor.tag_config("int", foreground=INTCOLOR)
editor.tag_config("func", foreground=FUNCCOLOR)
editor.pack(fill=BOTH, expand=True)

# status bar containing current file and character
status_frame = Frame(root, bg=STATUSCOLOR)
file_lbl = Label(status_frame, text="no file loaded!", bg=STATUSCOLOR, fg=TEXTCOLOR, font=FIRACODE)
file_lbl.pack(side=LEFT)
char_lbl = Label(status_frame, text="line 1 : char 0", bg=STATUSCOLOR, fg=TEXTCOLOR, font=FIRACODE)
char_lbl.pack(side=RIGHT)

# command bar at the bottom
command_frame = Frame(root, bg=BGCOLOR)
command_lbl = Label(command_frame, text="command line : ", bg=BGCOLOR, fg=TEXTCOLOR, font=FIRACODE)
command_lbl.pack(side=LEFT)
command_txt = Entry(command_frame, bg=BGCOLOR, fg=TEXTCOLOR, font=FIRACODE, highlightthickness=0, relief=FLAT, insertbackground=TEXTCOLOR)
command_txt.pack(side=RIGHT, fill=BOTH, expand=True)

# placing the frames
main_frame.grid(column=0, row=0, sticky="nsew")
status_frame.grid(column=0, row=1, sticky="nsew")
command_frame.grid(column=0, row=2, sticky="nsew")

# checking the syntax written on each keypress
root.bind("<KeyRelease>", check_syntax)
root.bind("<Button-1>", get_cursor_position)

# closing the main loop
root.mainloop()
