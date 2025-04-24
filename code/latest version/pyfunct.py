
import tkinter as tk

class Get(object):

    def __init__(self, master):
        #Get size of widget
        self.master = master

    def x(self):
        return self.master.winfo_width()

    def y(self):
        return self.master.winfo_height()

    def width(self):
        return eval(str(self.master['width']))

    def height(self):
        return eval(str(self.master['height']))


class ActiveLeave(object):

    def __init__(self, widget, bg='blue', fg='dark grey', bordure=0):
        #Color effect when cursor is hover the widget
        self.wdt = widget
        self.bg_ = widget.cget('background')
        self.bg = bg
        self.fg_ = widget.cget('foreground')
        self.fg = fg
        self.bd_ = widget.cget('bd')
        self.bd = bordure
        self.con_ = widget.cget('highlightcolor')
        Assign(self.wdt, self.leave, ['Leave'])
        Assign(self.wdt, self.enter, ['Enter'])

    def leave(self, event=None):
        self.wdt.config(bg=self.bg_, fg=self.fg_, bd=self.bd_, highlightcolor=self.con_)

    def enter(self, event=None):
        self.wdt.config(bg=self.bg, fg=self.fg, bd=self.bd, highlightcolor=self.con_)


class Popup(tk.Menu):

    def __init__(self, master, bind=['Button-3'], *cnf, **kwargs):
        tk.Menu.__init__(self, master, *cnf, **kwargs)
        Assign(master, self.popup, bind)

    def popup(self, event):
        try:
            self.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.grab_release()
        self.eventX = event.x
        self.eventY = event.y


class Assign(object):

    def __init__(self, mil, definit, touche=[]):
        self.m = mil
        self.d = definit
        self.t = touche
        for ww in self.t:
            self.m.bind('<{}>'.format(ww), self.d)

    def modifie(self, mil=None, definit=None, touche=[]):
        if mil != None:
            self.m = mil
        if definit != None:
            self.d = definit
        if touche != []:
            self.t = touche
        for ww in self.t:
            self.m.bind('<{}>'.format(ww), self.d)


COLORS = {
    "--dark-color": "#212529",
    "--light-color": "#fff",
    "--light-light-color": "#ebf1f1",
    "--dark-orange": "#ff5436",
    "--light-orange": "#ff8975",
    "--dark-turquoise": "#50e3c2",
    "--light-turquoise": "#59ebcb",
    "--dark-color-1": "#2c3f50",
    "--light-color-1": "#34495e",
    "--dark-cyan": "#00abcf",
    "--light-cyan": "#07b7dc",
    "--dark-orange-1": "#a45a37",
    "--light-orange-1": "#f2b597",
    "--dark-olive": "#0a3b47",
    "--light-olive": "#1a5c6c",
    "--dark-pale-green": "#a1abb0",
    "--light-pale-green": "#b0b791",
    "--dark-light-blue": "#7da4e3",
    "--light-light-blue": "#98bbf5",
    "--dark-blue": "#008fff",
    "--light-blue": "#45adff",
    "--dark-green": "#a4c013",
    "--light-green": "#bddb0b",
    "--dark-purple": "#6200ee",
    "--light-purple": "#bb86fc",
    "--dark-yellow": "#e7a930",
    "--light-yellow": "#e6bc43",
    "--dark-light-color": "#bec3c7",
    "--dark-pink": "#df65a0",
    "--light-pink": "#e77baf",
    "--dark-move": "#2520de",
    "--light-move": "#6c68ff",
    "--dark-green-1": "#27903c",
    "--light-green-1": "#36b64f",
    "--dark-orange-2": "#ff8d2c",
    "--light-orange-2": "#fea255",
    "--dark-olive-1": "#046262",
    "--light-olive-1": "#1f8384",
    "--dark-pink-1": "#e054b8",
    "--light-pink-1": "#ff74d9",
    "--dark-red": "#e23d4d",
    "--light-red": "#ec6170"
}

