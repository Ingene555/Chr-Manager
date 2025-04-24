import pyfunct as pf
import tkinter as tk
from tkinter.font import Font
import tkinter.ttk as ttk

MAX = 0
while True:
    try:
        MAX += 1
        chr(MAX)
    except:
        break


def getchr(value):
    try:a = str(chr(value))
    except:a = ''
    return a


class Binary:

    def __init__(self, master, function=None):
        self.master = master
        self.wdt = int(eval(str(pf.Get(self.master).width())))
        self.hgt = int(eval(str(pf.Get(self.master).height())))
        self.row = 1
        self.list = list()
        self.obj = list()
        self.rec = list()
        self.over, self.active = pf.COLORS['--light-color-1'], pf.COLORS['--dark-color-1']
        self.bg, self.fg = pf.COLORS['--dark-color'], pf.COLORS['--light-color']
        self.selected = 0
        self.func = function
        for ww in range(425):
            self.list.append(getchr(ww))
        a = 0
        for ww in range(17):
            for xx in range(25):
                self.rec.append(self.master.create_rectangle(self.wdt / 25 * xx, self.hgt / 17 * ww,
                                                             self.wdt / 25 * (xx + 1), self.hgt / 17 * (ww + 1),
                                                             width=0, fill=pf.COLORS['--dark-color']))
                self.obj.append(self.master.create_text(self.wdt / 25 * (xx + .5), self.hgt / 17 * (ww + .5),
                                                        text=getchr(a), justify=tk.CENTER,
                                                        font=Font(size=int(9), family='times'),
                                                        fill=pf.COLORS['--light-color']))
                a += 1
        self.master.itemconfig(self.rec[0], fill=self.active)
        self.master.tag_bind(tk.ALL, '<Enter>', self.tohand)
        self.master.tag_bind(tk.ALL, '<Leave>', self.toarrow)
        self.master.tag_bind(tk.ALL, '<Button-1>', self.leftClick)
        self.menu = pf.Popup(self.master, tearoff=False, bg=self.bg, fg=self.fg, activebackground=self.over,
                           relief=tk.SUNKEN, bd=0, border=0)
        self.menu.add_command(label='Copy character', command=self.copy)
        self.menu.add_command(label='Copy code point', command=self.copyCodePoint)
        pf.Assign(self.master, self.bigUp, ['Button-5'])
        pf.Assign(self.master, self.bigDown, ['Button-4'])
                
    def setRow(self, row=1):
        self.row = row
        if self.row < 1:
            self.row = 2622
        elif self.row > 2622:
            self.row = 1
        del(self.list[:])
        a = 0
        for ww in range(425 * (self.row - 1), 425 * self.row):
            self.list.append(str(getchr(ww)))
            self.master.itemconfig(self.obj[a], text=self.list[a])
            a += 1
        self.checkWhatToBind()
        if self.func:
            self.func(ord(self.list[self.selected]), self.list[self.selected], ord(self.list[self.selected]) // 425 + 1)
    
    def checkWhatToBind(self):
        self.master.tag_unbind(tk.ALL, '<Enter>')
        self.master.tag_unbind(tk.ALL, '<Leave>')
        self.master.tag_unbind(tk.ALL, '<Button-1>')
        for ww in range(425):
            if self.list[ww] != '':
                self.master.tag_bind(self.rec[ww], '<Enter>', self.tohand)
                self.master.tag_bind(self.rec[ww], '<Leave>', self.toarrow)
                self.master.tag_bind(self.rec[ww], '<Button-1>', self.leftClick)
                self.master.tag_bind(self.obj[ww], '<Enter>', self.tohand)
                self.master.tag_bind(self.obj[ww], '<Leave>', self.toarrow)
                self.master.tag_bind(self.obj[ww], '<Button-1>', self.leftClick)
    
    def selectObject(self, index):
        if index > MAX:
            index = MAX
        self.setRow((index - 1) // 425 + 1)
        self.selected = index % 425 - 1
        self.setTheme(self.bg, self.fg, self.over, self.active)
        if self.func:
            self.func(ord(self.list[self.selected]), self.list[self.selected], ord(self.list[self.selected]) // 425 + 1)
        return index
    
    def up(self, event=None):
        try:a = ord(self.list[self.selected])
        except:a = MAX
        if a - 24 < 0:
            a = MAX + 25
        return self.selectObject(a - 24)
    
    def down(self, event=None):
        try:a = ord(self.list[self.selected])
        except:a = MAX
        if a + 26 > MAX:
            a = -25
        return self.selectObject(a + 26)
    
    def left(self, event=None):
        try:a = ord(self.list[self.selected])
        except:a = MAX
        if a <= 0:
            a = 1114113
        return self.selectObject(a)
    
    def right(self, event=None):
        try:a = ord(self.list[self.selected])
        except:a = MAX
        if a + 2 > MAX:
            a = -1
        return self.selectObject(a + 2)
    
    def setTheme(self, bg=pf.COLORS['--dark-color-1'], fg=pf.COLORS['--light-color'], over=pf.COLORS['--light-color-1'], active=pf.COLORS['--dark-color']):
        self.bg = bg
        self.fg = fg
        self.over = over
        for ww in range(425):
            self.master.itemconfig(self.rec[ww], fill=bg)
            self.master.itemconfig(self.obj[ww], fill=fg)
        self.master.itemconfig(self.rec[self.selected], fill=self.active)
    
    def tohand(self, event=None):
        self.master['cursor'] = 'hand2'
        self.setTheme(self.bg, self.fg, self.over, self.active)
        item = self.master.find_closest(event.x, event.y)[0]
        if item in self.rec:
            i = self.rec.index(item)
        else:
            i = self.obj.index(item)
        self.master.itemconfig(self.rec[i], fill=self.over)
    
    def toarrow(self, event=None):
        self.master['cursor'] = 'arrow'
        self.setTheme(self.bg, self.fg, self.over, self.active)
    
    def leftClick(self, event=None):
        item = self.master.find_closest(event.x, event.y)[0]
        if item in self.rec:
            i = self.rec.index(item)
        else:
            i = self.obj.index(item)
        self.selected = i
        self.setTheme(self.bg, self.fg, self.over, self.active)
        if self.func:
            self.func(ord(self.list[self.selected]), self.list[self.selected], ord(self.list[self.selected]) // 425 + 1)
    
    def copy(self):
        root = self.master.winfo_toplevel()
        root.clipboard_clear()
        root.clipboard_append(self.list[self.selected])
    
    def copyCodePoint(self):
        root = self.master.winfo_toplevel()
        root.clipboard_clear()
        root.clipboard_append(ord(self.list[self.selected]))
    
    def bigUp(self, event=None):
        self.setRow(self.row - 1)
    
    def bigDown(self, event=None):
        self.setRow(self.row + 1)
    
    def getSelected(self, event=None):
        return [self.list[self.selected], self.obj[self.selected], self.rec[self.selected], ord(self.list[self.selected])]


class Container(tk.Toplevel, tk.Tk):

    def __init__(self, master=None, entry=None, theme=[pf.COLORS['--dark-color'], pf.COLORS['--light-color'], pf.COLORS['--light-color-1'], pf.COLORS['--dark-color-1']], *cnf, **kwargs):
        self.master = master
        self.entry = entry
        self.theme = theme
        if self.master:tk.Toplevel.__init__(self, master, *cnf, **kwargs)
        else:tk.Tk.__init__(self, *cnf, **kwargs)
        self.wm_attributes('-toolwindow', True)
        self.wm_attributes('-topmost', True)
        self.grab_set()
        self.protocol('WM_DELETE_WINDOW', self.close_modal_window)
        self.title('Chr Manager')
        self['bg'] = self.theme[0]
        self.geometry('900x550')
        self.resizable(False, False)
        
        self.topFrame = tk.Frame(self, width=830, height=80, border=0, bd=0, highlightthickness=0, relief=tk.SUNKEN, bg=self.theme[0])
        self.topFrame.grid(row=1, column=1)
        self.bleft = tk.Button(self.topFrame, text='<', bg=self.theme[0], fg=self.theme[1],
                  bd=0, border=0, relief=tk.SUNKEN, highlightthickness=0, cursor='hand2',
                  font=Font(family='courier_new', size=15), activebackground=self.theme[3],
                  activeforeground=pf.COLORS['--light-green'], command=self.left)
        self.bright = tk.Button(self.topFrame, text='>', bg=self.theme[0], fg=self.theme[1],
                  bd=0, border=0, relief=tk.SUNKEN, highlightthickness=0, cursor='hand2',
                  font=Font(family='courier_new', size=15), activebackground=self.theme[3],
                  activeforeground=pf.COLORS['--light-green'], command=self.right)
        pf.ActiveLeave(self.bleft, self.theme[2], pf.COLORS['--light-green'])
        pf.ActiveLeave(self.bright, self.theme[2], pf.COLORS['--dark-green'])
        self.indVar = tk.IntVar(value=0)
        self.chrVar = tk.StringVar(value=str(chr(0)))
        self.rowVar = tk.StringVar(value='Group' + ' 0 - 424')
        self.entrIndex = tk.Entry(self.topFrame, textvariable=self.indVar, width=15, bg=self.theme[2], fg=self.theme[1],
                  bd=0, border=0, relief=tk.SUNKEN, highlightthickness=0, disabledbackground=self.theme[0],
                  disabledforeground=self.theme[1], font=Font(size=12, family='times'), state='disabled')
        self.entrChar = tk.Entry(self.topFrame, textvariable=self.chrVar, width=15, bg=self.theme[2], fg=self.theme[1],
                  bd=0, border=0, relief=tk.SUNKEN, highlightthickness=0, disabledbackground=self.theme[0],
                  disabledforeground=self.theme[1], font=Font(size=12, family='times'), state='disabled')
        self.bleft.grid(row=1, column=1, sticky=tk.NS, rowspan=2)
        self.bright.grid(row=1, column=3, sticky=tk.NS, rowspan=2)
        self.entrIndex.grid(row=1, column=2)
        self.entrChar.grid(row=2, column=2)
        tk.Frame(self.topFrame, width=75, border=0, bd=0, highlightthickness=0, relief=tk.SUNKEN, bg=self.theme[0]).grid(row=1, column=4)
        self.cbbg = tk.Canvas(self.topFrame, width=320, height=80, border=0, bd=0, highlightthickness=0, relief=tk.SUNKEN, bg=self.theme[0])
        option = []
        for ww in range(2622):
            option.append('Group' + '  %s - %s' % (ww * 425, ((ww + 1) * 425) - 1))
        self.cbbg.grid(row=1, column=5, rowspan=2)
        self.rowVar.set(option[0])
        cbl = tk.Button(self.cbbg, text='<<', bg=self.theme[0], fg=self.theme[1],
                  bd=0, border=0, relief=tk.SUNKEN, highlightthickness=0, cursor='hand2',
                  font=Font(family='courier_new', size=11), activebackground=self.theme[3],
                  activeforeground=pf.COLORS['--light-green'])
        cbr = tk.Button(self.cbbg, text='>>', bg=self.theme[0], fg=self.theme[1],
                  bd=0, border=0, relief=tk.SUNKEN, highlightthickness=0, cursor='hand2',
                  font=Font(family='courier_new', size=11), activebackground=self.theme[3],
                  activeforeground=pf.COLORS['--light-green'])
        self.cbb = ttk.Combobox(self.cbbg, values=option, textvariable=self.rowVar, background=self.theme[0], state='disabled', cursor='hand2')
        cbl.grid(row=1, column=1)
        cbr.grid(row=1, column=3)
        self.cbb.grid(row=1, column=2, sticky=tk.EW)
        f = tk.Frame(self.topFrame, width=260, border=0, bd=0, highlightthickness=0, relief=tk.SUNKEN, bg=self.theme[0])
        f.grid(row=1, column=6)
        pf.Assign(self.entrIndex, self.enableIndex, ['Button-1'])
        pf.Assign(self.entrIndex, self.chooseIndex, ['Return'])
        pf.Assign(self.entrChar, self.enableChar, ['Button-1'])
        pf.Assign(self.entrChar, self.chooseChar, ['Return'])
        pf.Assign(self.cbb, self.enableRow, ['Button-1'])
        pf.Assign(self.cbb, self.chooseRow, ['<ComboboxSelected>'])
        
        self.can = tk.Canvas(self, width=820, height=500, border=0, bd=0, highlightthickness=0, relief=tk.SUNKEN, bg=self.theme[0])
        self.can.grid(row=2, column=1, padx=0)
        self.bin = Binary(self.can, self.function)
        pf.Assign(self, self.bin.up, ['Up'])
        pf.Assign(self, self.bin.down, ['Down'])
        pf.Assign(self, self.bin.left, ['Left'])
        pf.Assign(self, self.bin.right, ['Right'])
        cbl['command'] = self.bin.bigUp
        cbr['command'] = self.bin.bigDown
        pf.ActiveLeave(cbl, self.theme[2], pf.COLORS['--light-green'])
        pf.ActiveLeave(cbr, self.theme[2], pf.COLORS['--dark-green'])
        
        self.frame = tk.Frame(self, width=70, height=590, border=0, bd=0, highlightthickness=0, relief=tk.SUNKEN, bg=self.theme[0])
        self.frame.grid(row=1, column=2, rowspan=2)
        self.c = tk.Canvas(self.frame, width=70, height=70, border=0, bd=0, highlightthickness=0, relief=tk.SUNKEN, bg=self.theme[0])
        self.citem = self.c.create_text(35, 35, text=str(chr(1)), font=Font(size=35, family='times', weight='bold'), fill=self.theme[1])
        self.c.grid(row=1, column=1, sticky=tk.NSEW, padx=5)
        
        tk.Frame(self.frame, width=70, height=390, border=0, bd=0, highlightthickness=0, relief=tk.SUNKEN, bg=self.theme[0]).grid(row=2, column=1)
        b1 = tk.Button(self.frame, text='Copy', bg=self.theme[0], fg=self.theme[1],
                  bd=0, border=0, relief=tk.SUNKEN, highlightthickness=0, cursor='hand2',
                  font=Font(family='courier_new', size=12), activebackground=self.theme[3],
                  activeforeground=pf.COLORS['--light-blue'], command=self.bin.copy)
        b2 = tk.Button(self.frame, text='Close', bg=self.theme[0], fg=self.theme[1],
                  bd=0, border=0, relief=tk.SUNKEN, highlightthickness=0, cursor='hand2',
                  font=Font(family='courier_new', size=12), activebackground=self.theme[3],
                  activeforeground=pf.COLORS['--dark-orange'], command=self.close_modal_window)
        pf.ActiveLeave(b2, self.theme[2], pf.COLORS['--dark-red'])
        pf.ActiveLeave(b1, self.theme[2], pf.COLORS['--dark-blue'])
        b1.grid(row=3, column=1, sticky=tk.EW, pady=3)
        b2.grid(row=4, column=1, sticky=tk.EW, pady=3)
        pf.Assign(self, self.setDis, ['Button-1'])
    
    def close_modal_window(self):
        self.grab_release()
        self.quit()
        if self.entry:
            self.entry['stat'] = 'normal'
    
    def insert(self, event=None):
        if self.entry:
            a = self.entry['stat']
            self.entry['stat'] = 'normal'
            char = self.bin.list[self.bin.selected]
            index = self.entry.index(tk.INSERT)
            self.entry.insert(index, char)
            self.entry['stat'] = a
    
    def setDisabled(self, event=None):
        self.entrChar['stat'] = 'disabled'
        self.entrIndex['stat'] = 'disabled'
        self.cbb['stat'] = 'disabled'
    
    def setDis(self, event):
        if not event.widget in [self.entrChar, self.entrIndex, self.cbb]:
            self.entrChar['stat'] = 'disabled'
            self.entrIndex['stat'] = 'disabled'
            self.cbb['stat'] = 'disabled'
    
    def left(self):
        self.bin.left()
        self.indVar.set(self.bin.getSelected()[3])
        self.chrVar.set(self.bin.getSelected()[0])
        self.rowVar.set(self.cbb.cget('values')[self.bin.getSelected()[3] // 425])
        self.setDisabled()
    
    def right(self):
        self.bin.right()
        self.indVar.set(self.bin.getSelected()[3])
        self.chrVar.set(self.bin.getSelected()[0])
        self.rowVar.set(self.cbb.cget('values')[self.bin.getSelected()[3] // 425])
        self.setDisabled()
    
    def chooseIndex(self, event=None):
        self.bin.selectObject(int(self.indVar.get()) + 1)
        self.setDisabled()
    
    def enableIndex(self, event=None):
        self.setDisabled()
        self.entrIndex['stat'] = 'normal'
    
    def chooseChar(self, event=None):
        self.bin.selectObject(ord(self.chrVar.get()) + 1)
        self.setDisabled()
    
    def enableChar(self, event=None):
        self.setDisabled()
        self.entrChar['stat'] = 'normal'
    
    def chooseRow(self, event=None):
        self.bin.setRow(self.cbb.cget('values').index(self.rowVar.get()) + 1)
        self.setDisabled()
    
    def enableRow(self, event=None):
        self.setDisabled()
        self.cbb['stat'] = 'readonly'
    
    def function(self, index, char, row):
        self.indVar.set(index)
        self.chrVar.set(char)
        self.rowVar.set(self.cbb.cget('values')[row - 1])
        self.c.itemconfig(self.citem, text=char)

        
if __name__ == "__main__":
    Container().mainloop()

