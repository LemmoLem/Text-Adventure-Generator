import tkinter as tk
from tkinter import ttk

# file for UI implementation

# Top level window
frame = tk.Tk()
x = 1200
y = 600
frame.geometry('800x650')
frame.title("Text Adventure Game Generator")
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

# create a scrollbar widget and set its command to the text widget
scrollbar = ttk.Scrollbar(frame, orient='vertical' )
scrollbar.pack(side="right", fill="y")

# text outputted to player
game_text_box = tk.Text(frame, height=25, width=70, wrap="word")
game_text_box.pack(side="top", fill="x")
game_text_box.config(state="disabled")


text_box_options = tk.Text(frame, height=6, width=70, wrap="word")
text_box_options.pack(side="top", fill="x")
text_box_options.config(state="disabled")

# TextBox Creation
input_text = tk.Text(frame, height=5, width=70)
input_text.pack(side="top", fill="x")

# button creation
var = tk.IntVar()
button_to_enter = tk.Button(frame, text="Click me to input", command=lambda: var.set(1))
button_to_enter.pack(side="top")

#  set scrollbr to change y of textbox
scrollbar.config(command=game_text_box.yview)
game_text_box['yscrollcommand'] = scrollbar.set

def print_to_game_text(*args):
    string = ""
    for arg in args:
        if arg == None:
            string = string
        else:
            string += " " + arg
    game_text_box.config(state="normal")
    quote = string
    print(string)
    game_text_box.insert(tk.END, quote + "\n")
    game_text_box.yview_moveto(1.0)
    game_text_box.config(state="disabled")

def print_to_choices_box(*args):
    text_box_options.config(state="normal")
    text_box_options.delete("1.0", "end")
    string = ""
    for arg in args:
        string += " " + arg
    quote = string
    print(string)
    text_box_options.insert(tk.END, quote + "\n")
    text_box_options.yview_moveto(1.0)
    text_box_options.config(state="disabled")

def get_input(string):
    # print what game wants in input
    print_to_choices_box(string)
    button_to_enter.wait_variable(var)
    inp = get_content_from_input()
    # has to wait for user to press button
    return inp

def enter_key(event):
    button_to_enter.invoke()
# bind enter key to function which just calls the function that happens when button is pressed
frame.bind('<Return>', enter_key)

def get_content_from_input():
    # print input
    inp = input_text.get(1.0, "end-1c")
    inp = inp.strip("\n")
    # delete what was in the box
    input_text.delete("1.0", "end")
    return inp

def frame_main_loop():
    frame.mainloop()


line_length = 1000
break_line_str = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

