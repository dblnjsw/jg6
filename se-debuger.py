import se_chicme
from se_chicme import Se_chicme
import tkinter as tk
from threading import Thread
from functools import partial
from tkinter import messagebox
import json
import os
from importlib import reload
import atexit
import inspect
import types
from PIL import Image
from PIL import ImageTk
from time import sleep

ch_group = {}
sections = []
map_section_name_button = {}
map_section_name_value = {}
map_function_name_button = {}
map_currentChromes_name_rbutton = {}
win = tk.Tk()
v_currentChromes = tk.IntVar()
names = locals()
csection = None
image = None
im = None
text_locate = tk.StringVar()


@atexit.register
def exit():
    print('exit')
    with open('se-records.txt', 'w', encoding='UTF-8') as f:
        js = json.dumps(map_section_name_value)
        f.write(js)


class Execer():
    scope = {}

    def ex(self, lines):
        print('section start:\n' + str(lines))
        lines = lines.split('\n')
        global names
        for l in lines:
            l = l.replace(' ', '')
            l = l.replace('\n', '')
            l = l.replace('\t', '')

            if 'Se_chicme' in l:
                ls = l.split('=', 1)

                l = 'names["' + ls[0] + '"]=' + ls[1]
                v = len(map_currentChromes_name_rbutton)
                map_currentChromes_name_rbutton[ls[0]] = tk.Radiobutton(lf_functions, text=ls[0],
                                                                        variable=v_currentChromes, value=v)
                map_currentChromes_name_rbutton[ls[0]].pack()
                win.update()
                exec(l)
                ch_group[ls[0]] = names[ls[0]]
            else:
                exec(l)

        print('section over')

        # print(lines)


execer = Execer()


def b_run():
    global execer
    lines = textarea.get('1.0', tk.END)
    t = Thread(target=execer.ex, args=(lines,))
    t.start()


def b_locate():
    global im
    global image
    prefix=None
    i = 0
    text_locate.set('正在定位。。。')
    for e in map_currentChromes_name_rbutton:
        if v_currentChromes.get() == i:
            prefix = e
            break
        i += 1
    element=ch_group[prefix].find_element_by_xpath(e_locate_xpath.get())
    if element:
        text_locate.set('定位成功')
    else:
        text_locate.set('定位失败')
        return
    image = Image.open("locate.png")
    im = ImageTk.PhotoImage(image)
    c_locate.create_image(300, 300,image=im)

    c_locate.pack()
    win.update()
    pass


def b_new():
    name = b_new_name.get()
    if name in map_section_name_button:
        raise AssertionError('命名重复')
    b_new_name.delete(0, tk.END)
    b_s = tk.Button(lf_sections, text=name, command=partial(b_section, name))
    b_s.pack()
    win.update()
    map_section_name_button[name] = b_s
    map_section_name_value[name] = ''


def b_delete():
    global csection
    map_section_name_value.pop(csection)
    map_section_name_button[csection].destroy()
    win.update()
    map_section_name_button.pop(csection)


def b_section(name):
    global csection
    csection = name
    textarea.delete('1.0', tk.END)
    textarea.insert(tk.END, map_section_name_value[name])


def b_function(name):
    textarea.delete('1.0', tk.END)
    prefix = 'chicme.'
    i = 0
    for e in map_currentChromes_name_rbutton:
        if v_currentChromes.get() == i:
            prefix = e + '.'
            break
        i += 1

    textarea.insert(tk.END, prefix + name + '()')


def b_save():
    map_section_name_value[csection] = textarea.get('1.0', tk.END)


def b_reload():
    reload(se_chicme)
    reload_functions()
    for e in ch_group:
        c_replaced = ch_group[e]
        c = se_chicme.Se_chicme(driver=c_replaced.wd, headless=c_replaced.headless, msite=c_replaced.msite)
        names[e] = c
        ch_group[e] = c
    messagebox.showinfo(message='reload suceess')


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        with open('se-records.txt', 'w', encoding='UTF-8') as f:
            js = json.dumps(map_section_name_value)
            f.write(js)
        win.destroy()


def key_ctrl_z(event):
    textarea.edit_undo()


def callback(event):
    textarea.edit_separator()


def key_enter(event):
    b_new()


def reload_functions():
    for b in map_function_name_button:
        map_function_name_button[b].destroy()
    for item, t in inspect.getmembers(se_chicme.Se_chicme):
        if type(t) is types.FunctionType and not item.startswith('_'):
            b = tk.Button(lf_functions, text=item, command=partial(b_function, item))
            b.pack()
            map_function_name_button[item] = b
    win.update()


changeFlag = False
# c=Se_chicme()

win.title('se-debuger v1.0')
win.geometry('1360x800')

win.protocol("WM_DELETE_WINDOW", on_closing)
# out
lf_out = tk.LabelFrame(win)
lf_out.pack(side=tk.RIGHT, fill=tk.Y)
# l_out_current_seciton_text = tk.Label(lf_out, text='current section:')
# l_out_current_seciton = tk.Label(lf_out)

b = tk.Button(lf_out, text='run', command=b_run)
b_out_save = tk.Button(lf_out, text='save', command=b_save)
b_out_reload = tk.Button(lf_out, text='reload', command=b_reload)
# l_out_current_seciton_text.pack()
# l_out_current_seciton.pack()

b_out_save.pack()
b_out_reload.pack()
b.pack()

textarea = tk.Text(lf_out, undo=True, autoseparators=False)
textarea.bind('<Control-z>', key_ctrl_z)
textarea.bind('<Key>', callback)
vscroll = tk.Scrollbar(lf_out, orient=tk.VERTICAL, command=textarea.yview)
textarea['yscroll'] = vscroll.set
vscroll.pack(side=tk.RIGHT, fill=tk.Y)
textarea.pack(fill=tk.Y, side=tk.RIGHT)

# sections
lf_sections = tk.LabelFrame(win, text='sections')
lf_sections_action = tk.LabelFrame(lf_sections, text='action')
b_new_section = tk.Button(lf_sections_action, text='new', command=b_new)
b_delete_section = tk.Button(lf_sections_action, text='delete', command=b_delete)
b_new_name = tk.Entry(lf_sections)
b_new_name.bind('<Return>', key_enter)

lf_sections.pack(side=tk.LEFT, fill=tk.Y)
b_new_name.pack()
lf_sections_action.pack()

# functions
lf_functions = tk.LabelFrame(win, text='functions')
lf_functions.pack(side=tk.LEFT, fill=tk.Y)

b_new_section.pack(side=tk.LEFT)
b_delete_section.pack(side=tk.RIGHT)

# locate
lf_locate = tk.LabelFrame(win, text='locate')
lf_locate.pack(side=tk.LEFT, fill=tk.Y)

e_locate_xpath = tk.Entry(lf_locate)
b_locate_b = tk.Button(lf_locate, text='locate', command=b_locate)
l_locate=tk.Label(lf_locate,textvariable=text_locate)
# text_locate.set('未找到')
c_locate = tk.Canvas(lf_locate,height=600,width=600)

# image = Image.open("paypal.png")
# im=ImageTk.PhotoImage(image)
# c_locate.create_image(500,500,image=im)


e_locate_xpath.pack()
b_locate_b.pack()
l_locate.pack()
# c_locate.pack()


# init
if os.path.exists('se-records.txt'):
    with open('se-records.txt', 'r', encoding='UTF-8') as f:
        s = f.read()
        map_section_name_value = json.loads(s)
    for e in map_section_name_value:
        b = tk.Button(lf_sections, text=e, command=partial(b_section, e))
        b.pack()
        map_section_name_button[e] = b

reload_functions()

win.mainloop()
