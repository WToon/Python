from tkinter import *

import tkinter.filedialog
import os

__author__ = "Toon Willemot"

" Some global variables and basic initialization "

PROGRAM_NAME = 'Footprint Editor'
root = Tk()
root.title(PROGRAM_NAME)
root.geometry('{}x{}'.format(1200, 700))
file_name = None

# --------------------------|
#        Functionality      |
# --------------------------|


def change_theme(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    foreground_color, background_color = fg_bg_colors.split('.')
    content_text.config(background=background_color,
                        fg=foreground_color)


def on_content_changed(event=None):
    update_line_numbers()
    update_cursor_info_bar()


def show_cursor_info_bar():
    show_cursor_info_checked = show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None,
                             side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()


def update_cursor_info_bar(event=None):
    row, col = content_text.index(INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col)+1)
    info_text = "Line: {0} | Column {1}".format(line_num, col_num)
    cursor_info_bar.config(text=info_text)


def highlight_line(interval=100):
    content_text.tag_remove("active_line", 1.0, 'end')
    content_text.tag_add('active_line',
                         "insert linestart",
                         "insert lineend+1c")
    content_text.after(interval, toggle_highlight)


def undo_highlight():
    content_text.tag_remove("active_line", 1.0, "end")


def toggle_highlight(event=None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()


def get_line_numbers():
    output = ''
    if show_line_no.get():
        row, col = content_text.index("end").split('.')
        for i in  range(1, int(row)):
            output += str(i)+ '\n'
    return output


def update_line_numbers():
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')


def new(event=None):
    root.title('Untiteld')
    global file_name
    file_name = None
    content_text.delete(1.0, 'end')
    on_content_changed()
    return


def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                                                         filetypes=[("All Files", "*.*"),
                                                                    ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{}-{}'.format(os.path.basename(file_name), PROGRAM_NAME))
        content_text.delete('1.0', END)
        with open(file_name) as _file:
            content_text.insert(1.0, _file.read())
    on_content_changed()
    return 'break'


def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return 'break'


def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
                                                           filetypes=[("All Files", "*.*"),
                                                                      ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{}-{}'.format(os.path.basename(file_name),
                                  PROGRAM_NAME))
    return 'break'


def write_to_file(name):
    try:
        content = content_text.get(1.0, 'end')
        with open(name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass


def exit_callback(event=None):
    quit()


def undo(event=None):
    content_text.event_generate("<<Undo>>")
    on_content_changed()
    return 'break'


def redo(event=None):
    content_text.event_generate("<<Redo>>")
    on_content_changed()
    return 'break'


def cut(event=None):
    content_text.event_generate("<<Cut>>")
    on_content_changed()
    return 'break'


def copy(event=None):
    content_text.event_generate("<<Copy>>")
    return 'break'


def paste(event=None):
    content_text.event_generate("<<Paste>>")
    return 'break'


def find(event=None):
    search_toplevel = Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="Find All: ").grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_toplevel, text='Ignore Case',
                variable=ignore_case_value).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(search_toplevel, text='Find All', underline=0,
           command=lambda: search_output(search_entry_widget.get(), ignore_case_value.get(), content_text,
                                         search_toplevel, search_entry_widget)
           ).grid(row=0, column=2, sticky='e'+'w', padx=2, pady=2)


    def close_search_window():
        print('clsoing')
        content_text.tag_remove('match', '1.0', END)
        search_toplevel.destroy()
    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return 'break'


def search_output(needle, if_ignore_case, content_text, search_toplevel, search_box):
    content_text.tag_remove('match', '1.0', END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle, start_pos, nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(needle))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        content_text.tag_config('match', foreground='red', background='yellow')
        search_toplevel.title('{} matches found'.format((matches_found)))


def select_all(event=None):
    content_text.tag_add('sel', '1.0', 'end')
    return 'break'


def help(event=None):
    search_toplevel = Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="The help menu isn't implemented fully yet").pack()


# ------------------|
#       Menus       |
# ------------------|

menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
edit_menu = Menu(menu_bar, tearoff=0)
view_menu = Menu(menu_bar, tearoff=0)
about_menu = Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
menu_bar.add_cascade(label='View', menu=view_menu)
menu_bar.add_cascade(label='About', menu=about_menu)

file_menu.add_command(label='New', accelerator='Ctrl + N', compound='left', command=new)
file_menu.add_command(label='Open', accelerator='Ctrl + O', compound='left', command=open_file)
file_menu.add_command(label='Save', accelerator='Ctrl + S', compound='left', command=save)
file_menu.add_command(label='Save as', accelerator='Shift + Ctrl + S', compound='left', command=save_as)
file_menu.add_separator()
file_menu.add_command(label='Exit', accelerator='Alt + F4', compound='left', command=exit_callback)

edit_menu.add_command(label='Undo', accelerator='Ctrl + Z', compound='left', command=undo)
edit_menu.add_command(label='Redo', accelerator='Ctrl + Y', compound='left', command=redo)
edit_menu.add_separator()
edit_menu.add_command(label='Cut', accelerator='Ctrl + X', compound='left', command=cut)
edit_menu.add_command(label='Copy', accelerator='Ctrl + C', compound='left', command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl + V', compound='left', command=paste)
edit_menu.add_separator()
edit_menu.add_command(label='Find', accelerator='Ctrl + F', compound='left', command=find)
edit_menu.add_command(label='Select All', accelerator='Ctrl + A', compound='left', command=select_all)

show_line_no = IntVar()
show_cursor_info = BooleanVar()
to_highlight_line = BooleanVar()
theme_choice = StringVar()
color_schemes = {'Default': '#000000.#FFFFFF',
                 'Greygarious':'#83406A.#D1D4D1',
                 'Aquamarine': '#5B8340.#D1E7E0',
                 'Bold Beige': '#4B4620.#FFF0E1',
                 'Cobalt Blue':'#ffffBB.#3333aa',
                 'Olive Green': '#D1E7E0.#5B8340',
                 'Night Mode': '#FFFFFF.#000000',
}
view_menu.add_checkbutton(label='Show Line Number', variable=show_line_no)
view_menu.add_checkbutton(label='Show Cursor Location', variable=show_cursor_info, command=show_cursor_info_bar)
view_menu.add_checkbutton(label='Highlight current line', variable=to_highlight_line, command=toggle_highlight)
themes_menu = Menu(view_menu, tearoff=0)
view_menu.add_cascade(label='Themes', menu=themes_menu)
for i in color_schemes:
    theme_name = color_schemes.get(i)
    themes_menu.add_radiobutton(label=i, variable=theme_choice, command=change_theme)

about_menu.add_command(label='Help', command=help)
about_menu.add_command(label='About')

# ----------------------------------------------|
#  Shortcuts, line numbers and main text widget |
# ----------------------------------------------|

shortcut_bar = Frame(root, height=25, background='light gray')
shortcut_bar.pack(expand='no', fill='x')

line_number_bar = Text(root, width=4, padx=3, takefocus=0, border=0, background='khaki', state='disabled', wrap='none')
line_number_bar.pack(side='left', fill='y')

content_text = Text(root, wrap='word', undo=1)
content_text.pack(expand='yes', fill='both')
content_text.bind('<Control-y>', redo)
content_text.bind('<Control-Y>', redo)
content_text.bind('<Control-a>', select_all)
content_text.bind('<Control-A>', select_all)
content_text.bind('<Control-f>', find)
content_text.bind('<Control-F>', find)
content_text.bind('<Control-N>', new)
content_text.bind('<Control-n>', new)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-S>', save)
content_text.bind('<Control-s>', save)
content_text.bind('<Any-KeyPress>', on_content_changed)
content_text.bind('<Button>', on_content_changed)

content_text.tag_configure('active_line', background='ivory2')

scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side='right', fill='y')

cursor_info_bar = Label(content_text, text='Line: 1 | Column: 1')
cursor_info_bar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')

popup_menu = Menu(content_text)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd=eval(i)
    popup_menu.add_command(label=i, compound='left', command=cmd)
popup_menu.add_separator()
popup_menu.add_command(label='Select All', underline=7, command=select_all)

# ------------------|
#       Vital       |
# ------------------|

root.config(menu=menu_bar)
root.mainloop()
