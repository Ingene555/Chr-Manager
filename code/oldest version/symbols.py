from pyfunct import *
import tkinter.ttk as ttk
from tkinter import *
from tkinter.scrolledtext import *
from tkinter.font import Font
from tkinter.messagebox import *
from os import *
from math import inf
from random import randrange

BITMAP = 'bitmap'
PHOTO = 'photo'


class Progression(ttk.Progressbar):

    def __init__(self, master, length=400, operation=None, *arg, **kwarg):
        self.top = Toplevel(master)
        ttk.Progressbar.__init__(self, self.top, length=length, *arg, *kwarg)
        s = ttk.Style(self.top)
        s.theme_use('clam')

        self.grid(row=1, column=1, columnspan=2, padx=20, pady=5)
        self.lab = ttk.Label(self.top, text=f"{self['value']} %")
        self.lab.grid(row=2, column=1, sticky=EW, padx=20)
        self.b_quit = ttk.Button(self.top, text='Cancel', command=self.stop_operation)
        self.b_quit.grid(row=2, column=2, padx=50)

        s.configure('TButton', font='TkDefaultFont 9')

        self.top.resizable(False, False)
        self.operation = operation
        self.top.mainloop()

    def progress(self, valeur):
        if self['value'] >= 100:
            self['value'] = 100
            print('End')
        self.lab['text'] = f"{self['value']} %"

    def stop_operation(self):
        if self.operation:
            self.operation()
        self.top.destroy()


class ActiveLeave(object):

    def __init__(self, widget, bg='blue', fg='dark grey', bordure=0, contour='navy blue'):
        self.wdt = widget
        self.bg_ = widget.cget('background')
        self.bg = bg
        self.fg_ = widget.cget('foreground')
        self.fg = fg
        self.bd_ = widget.cget('bd')
        self.bd = bordure
        self.con_ = widget.cget('highlightcolor')
        self.con = contour

        Assign(self.wdt, self.leave, ['Leave'])
        Assign(self.wdt, self.enter, ['Enter'])

    def leave(self, event=None):
        self.wdt.config(bg=self.bg_, fg=self.fg_, bd=self.bd_, highlightcolor=self.con_)

    def enter(self, event=None):
        self.wdt.config(bg=self.bg, fg=self.fg, bd=self.bd, highlightcolor=self.con)


'''✓✔✕☑✍☍♾❑⟲⟳❓❔ '''


class Chr(Canvas):

    def __init__(self, master=None, master_root=None, titre='Symbols', icon=None, icontype='bitmap', icon_n='', style='vista'):
        # interface utilisateur
        if master:
            top = Toplevel(master)
            top.wm_attributes('-toolwindow', True)
            top.transient(master)
            self.master = top
            self.master.title(titre)
        else:
            self.master = Tk()
            self.master.title(titre)
        if icontype == 'photo':
            self.master.iconphoto(False, PhotoImage(file=icon))
        elif icontype == 'bitmap':
            self.master.iconbitmap(icon)
        self.master_root = master_root
        if master_root:
            master_root.wm_attributes('-disabled', True)
            self.master.wm_attributes('-toolwindow', True)
        self.master.wm_attributes('-topmost', True)
        Canvas.__init__(self, self.master)
        self.grid(row=2, column=1, columnspan=5)
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.wtexte = master
        self.icontype = icontype
        self.title = titre
        self.icon = icon
        self.icon_n = icon_n
        self.stl = style

        self.master.protocol('WM_DELETE_WINDOW', self.quitter)

        # Liste pour le changement de langue
        ###########################
        # Menu principale
        self.pal_men = []
        self.pal_men_name = ['File', 'Edit', 'Help']

        # Menu fichier
        self.pal_men_fichier = []
        self.pal_men_fichier_name = ['Save the present character', 'Exit']

        # Menu application
        self.pal_men_appli = []
        self.pal_men_appli_name = ['Reset indexs', 'Reset fonts', 'Reset font size', 'Reset fonts', 'Reset backgrounds',
                                 'Reset highlights', 'Reset all', 'Copy character     ']

        # Menu aide
        self.pal_men_aide = []
        self.pal_men_aide_name = []

        # Interface chr
        self.pal_wdt_chr = []
        self.pal_wdt_chr_name = ['Characters']

        # Interface police
        self.pal_wdt_pol = []
        self.pal_wdt_pol_name = ['Fonts', 'Apply     ✓']

        # autre bouton 1
        self.pal_wdt_other = []
        self.pal_wdt_other_name = ['Reset     ⟲', 'Save     ✔', 'Copy     ', 'Insert     ✍', 'Fermer     ✕']

        # coomandes du texte chr
        self.pal_wdt_txt = []
        self.pal_wdt_txt_name = ['All characters with values', 'Combined normals', 'Characters only', 'Forward values', 'Copy characters...     ']

        # copie
        self.pal_wdt_copie = []
        self.pal_wdt_copie_name = ['Copying multiple characters', 'Situate the limits', 'Start', 'End', 'Line :', 'Column :', 'Cancel     ✗',
                                  'Copy interval     ', 'Copy all     ']

        # information
        self.pal_lb_about = []
        self.pal_lb_about_name = ['''- Title: Symbols
- Version: 1.0.0
- Release date: November 22/21''']

        # Menu
        self.menu = Menu (self.master, tearoff=0)
        self.master.configure(menu=self.menu)

        self.men_fichier = Menu(self.menu, tearoff=0)
        self.men_edition = Menu(self.menu, tearoff=0)
        self.men_help = Menu(self.menu, tearoff=0)
        self.pal_men.append(self.menu.add_cascade(label='File', menu=self.men_fichier))
        self.pal_men.append(self.menu.add_cascade(label='Edit', menu=self.men_edition))
        self.pal_men.append(self.menu.add_cascade(label='Help', menu=self.men_help))

        # menu file
        self.men_fichier.add_command(label='Save the present character', accelerator='✔     Ctrl+S', command=self.save)
        self.men_fichier.add_separator()
        self.men_fichier.add_command(label='Exit', accelerator='✕     Alt+F4', command=self.quitter)
        Assign(self.master, self.save, ['Control-S', 'Control-s'])
        Assign (self.master, self.quitter, ['Alt-F4'])
        # menu application
        self.pal_men_appli.append(self.men_edition.add_command(label='Reset indexs', accelerator='⟳     Shift+R', command=self.rest_index))
        self.pal_men_appli.append(self.men_edition.add_command(label='Reset fonts', accelerator='⟳     Alt+R', command=self.rest_pol))
        self.pal_men_appli.append(self.men_edition.add_command(label='Reset font size', accelerator='⟳     Shift+Ctrl+R', command=self.rest_size))
        self.pal_men_appli.append(self.men_edition.add_command(label='Reset fonts', accelerator='⟳     Alt+F', command=self.rest_text))
        self.pal_men_appli.append(self.men_edition.add_command(label='Reset backgrounds', accelerator='⟳     Shift+C', command=self.rest_bg))
        self.pal_men_appli.append(self.men_edition.add_command(label='Reset highlights', accelerator='⟳     Alt+C', command=self.rest_fg))
        self.pal_men_appli.append(self.men_edition.add_command(label='Reset all', accelerator='⟲     Ctrl+R', command=self.restart))
        self.men_edition.add_separator()
        self.pal_men_appli.append(self.men_edition.add_command(label='Copy character     ', command=self.copie))
        Assign (self.master, self.rest_index, ['Shift-R', 'Shift-r'])
        Assign (self.master, self.rest_pol, ['Alt-R', 'Alt-r'])
        Assign (self.master, self.rest_size, ['Shift-Control-R', 'Shift-Control-r'])
        Assign(self.master, self.rest_text, ['Alt-F', 'Alt-f'])
        Assign(self.master, self.rest_bg, ['Shift-C', 'Shift-c'])
        Assign(self.master, self.rest_fg, ['Alt-C', 'Alt-c'])
        Assign (self.master, self.restart, ['Control-R', 'Control-r'])

        # menu aide
        if not master:
            self.pal_men_aide.append(self.men_help.add_command(label='About the software', accelerator='❓     Alt+A', command=self.about))
            self.pal_men_aide_name.append('About the software')
            self.men_help.add_separator()
        self.pal_men_aide.append(self.men_help.add_command(label='About characters', accelerator='❔     Alt+C', command=self.caract))
        self.pal_men_aide_name.append('About characters')
        Assign (self.master, self.about, ['Alt-A', 'Alt-a'])
        Assign (self.master, self.caract, ['Alt-C', 'Alt-c'])
        self.ver = False
        self.car = False

        # LabelFrame 1 + Frame 1
        self.labf1 = ttk.Labelframe(self.master, labelanchor=NW, text='characters')
        self.pal_wdt_chr.append(self.labf1)
        self.frame1 = ttk.Frame(self.labf1)
        self.labf1.configure(labelwidget=self.frame1)
        self.labf1.grid(row=3, column=1, rowspan=5, padx=20, pady=20, sticky=EW)
        self.frame1.grid()
        ttk.Separator(self.master).grid(row=3, column=2, rowspan=5, sticky=NS)

        # LabelFrame 2 + Frame 2
        self.labf2 = ttk.Labelframe(self.master, labelanchor=NW, text='Fonts')
        self.pal_wdt_pol.append(self.labf2)
        self.frame2 = ttk.Frame(self.labf2)
        self.labf2.configure(labelwidget=self.frame2)
        self.labf2.grid(row=3, column=3, rowspan=5, padx=20, pady=20, sticky=EW)
        self.frame2.grid()
        ttk.Separator(self.master).grid(row=3, column=4, rowspan=5, sticky=NS)

        # Reinitialiser
        self.b_reset = ttk.Button(self.master, text='Reset     ⟲', command=self.restart)
        self.pal_wdt_other.append(self.b_reset)
        self.b_reset.grid(row=3, column=5, sticky=EW)

        # Enregistrement
        self.b_save = ttk.Button(self.master, text='Save     ✔', command=self.save)
        self.pal_wdt_other.append(self.b_save)
        self.b_save.grid(row=4, column=5, sticky=EW)
        
        # Copie.
        self.b_copie = ttk.Button(self.master, text='Copy     ', command=self.copie)
        self.pal_wdt_other.append(self.b_copie)
        self.b_copie.grid(row=5, column=5, sticky=EW)

        # Insertion
        self.b_insert = ttk.Button(self.master, text='Insert     ✍', command=self.inserer)
        self.pal_wdt_other.append(self.b_insert)
        self.b_insert.grid(row=6, column=5, sticky=EW)

        if not self.wtexte:
            self.b_insert.configure(state='disabled')

        # Fermer
        self.b_fermer = ttk.Button(self.master, text='Close    ✕', command=self.quitter)
        self.pal_wdt_other.append(self.b_fermer)
        self.b_fermer.grid(row=7, column=5, sticky=EW)

        # Interface de la police
        self.var_pol = StringVar(value='TkDefaultFont')
        self.comb_pol = ttk.Combobox(self.labf2, textvariable=self.var_pol, values=POLICE, stat='readonly')
        self.comb_pol.grid(row=1, column=1, columnspan=4, sticky=EW)
        self.var_size = StringVar(value=9)
        self.spn_size = ttk.Spinbox(self.labf2, textvariable=self.var_size, from_=1, to=inf, command=self.ch_pol, width=int(self.comb_pol.cget('width')))
        self.spn_size.grid(row=2, column=1, columnspan=4, sticky=EW)
        Assign(self.spn_size, self.ch_pol, ['Return'])

        self.b_gras = Checkbutton(self.labf2, text='', font=Font(weight='bold', family='Arial_Black'), command=self.gras, indicatoron=0,
                             relief=FLAT, bd=0, highlightthickness=0, width=2, selectcolor='blue', bg='light grey')
        ActiveLeave(self.b_gras, bg='dark blue', fg='light grey')
        self.b_gras.grid(row=3, column=1)
        self.var_gras = StringVar(value='normal')

        self.b_italic = Checkbutton(self.labf2, text='', font=Font(weight='bold', family='times', slant='italic'), command=self.italic, indicatoron=0,
                             relief=FLAT, bd=0, highlightthickness=0, width=2, selectcolor='blue', bg='light grey')
        ActiveLeave(self.b_italic, bg='dark blue', fg='light grey')
        self.b_italic.grid(row=3, column=2)
        self.var_italic = StringVar(value='roman')

        self.b_soul = Checkbutton(self.labf2, text='', font=Font(weight='bold', family='Arial_Black', underline=True), command=self.soul, indicatoron=0,
                             relief=FLAT, bd=0, highlightthickness=0, width=2, selectcolor='blue', bg='light grey')
        ActiveLeave(self.b_soul, bg='dark blue', fg='light grey')
        self.b_soul.grid(row=3, column=3)
        self.var_soul = False

        self.b_over = Checkbutton(self.labf2, text='abc', font=Font(overstrike=inf), command=self.over, indicatoron=0,
                             relief=FLAT, bd=0, highlightthickness=0, width=2, selectcolor='blue', bg='light grey')
        ActiveLeave(self.b_over, bg='dark blue', fg='light grey')
        self.b_over.grid(row=3, column=4)
        self.var_over = False

        self.b_fg = Button(self.labf2, text='A', font=Font(weight='bold', family='Arial_Black', underline=True), command=self.coul_fg,
                             relief=FLAT, bd=0, highlightthickness=0, width=2, fg='dark blue', bg='light grey')
        ActiveLeave(self.b_fg, bg='dark blue', fg='light grey')
        self.b_fg.grid(row=4, column=1)
        self.fg_ = 'SystemWindowText'
        self.b_bg = Button(self.labf2, text='⚫', font=Font(weight='bold', family='Arial_Black'), command=self.coul_bg,
                             relief=FLAT, bd=0, highlightthickness=0, width=2, fg='dark red', bg='light grey')
        ActiveLeave(self.b_bg, bg='dark blue')
        self.b_bg.grid(row=4, column=2)
        self.bg_ = '#777777'
        
        self.b_ch_pol = ttk.Button(self.labf2, text='Apply     ✓', command=self.appliquer, underline=0)
        self.pal_wdt_pol.append(self.b_ch_pol)
        self.b_ch_pol.grid(row=4, column=3, columnspan=2, sticky=EW)

        # Interface du caractère
        self.var_caract = StringVar(value=0)
        self.var_char = StringVar(value=chr(int(self.var_caract.get())))
        self.entr_caract = ttk.Entry(self.labf1, textvariable=self.var_char, width=15)
        self.entr_caract.grid(row=1, column=1, columnspan=2, sticky=EW)
        self.spn_caract = ttk.Spinbox(self.labf1, textvariable=self.var_caract, from_=0, to=1114111, command=self.ch_caract_spn, width=20)
        self.spn_caract.grid(row=1, column=2, columnspan=2, sticky=EW)
        Assign(self.spn_caract, self.ch_caract_spn, ['Return'])

        self.var_gbchr = StringVar(value=0)
        self.pal1 = list(range(0, 1114112, 425))
        self.pal1.append(1114111)
        self.lb_gbchr = Listbox(self.labf1, width=30, selectbackground='grey75', height=7)
        self.yb_lb = ttk.Scrollbar(self.labf1, command=self.lb_gbchr.yview)
        self.lb_gbchr.config(yscrollcommand=self.yb_lb.set)
        self.lb_gbchr.grid(row=2, column=1, columnspan=2, sticky=EW)
        self.yb_lb.grid(row=2, column=3, sticky=NS)
        Assign(self.lb_gbchr, self.selection, ['Button-1', 'ButtonRelease', 'Up', 'Down', 'KeyPress', 'KeyRelease'])

        self.pal = []
        self.pal_index = []
        for ww in self.pal1:
            if ww != self.pal1[len(self.pal1) - 1]:
                self.pal_index.append([ww, self.pal1[self.pal1.index(ww) + 1] - 1])
                self.pal.append(' %s - %s ' % (ww, self.pal1[self.pal1.index(ww) + 1] - 1))
        for ww in self.pal:
            self.lb_gbchr.insert(END, ww)
        self.lb_gbchr.select_set(0)

        def insert_chr(chr_):
            self.entr_caract.delete(0, END)
            self.entr_caract.insert(0, chr_)

        self.style.configure('TEntry', font='TkDefaultFont 9')
        self.pal_b = []
        self.var = StringVar(value=0)
        a = 1; b = 1
        for ww in range(425):
            if a > 25:
                a = 1
                b += 1
            c = Radiobutton(self, width=3, text=chr(ww), indicatoron=0, value=ww + 1, variable=self.var, font='%s %s' % (self.var_pol.get(), int(self.var_size.get())),
                                          relief=FLAT, bd=0, highlightthickness=2, selectcolor='light blue', bg='#777777',
                                          command=lambda arg=ww: insert_chr(chr(arg)))
            c.grid(row=b, column=a, sticky=NS)
            ActiveLeave(c)
            self.pal_b.append(c)
            a += 1

        #################################################
        #                                                                                                                             #
        self.master.resizable(False, False)  #                                                                     #
        #                                                                                                                               #
        #################################################
        self.f = chr(0)
        self.f_()
        self.pb = ''

        self.ver_insert = False
        self._entr_txt1, self.entr_txt2, self.entr_entr = '', '', ''
        self.ver_sc = False
        try: _h = Lire('{}\\DS config\\BGG Symbols.ini'.format(getcwd())).assigne()
        except: _h = c['bg']
        try: _g = Lire('{}\\DS config\\FGG Symbols.ini'.format(getcwd())).assigne()
        except: _g = c['fg']
        try: _a = Lire('{}\\DS config\\PFG Symbols.ini'.format(getcwd())).assigne()
        except: _a = self.var_pol.get()
        try: _b = Lire('{}\\DS config\\SG Symbols.ini'.format(getcwd())).assigne()
        except: _b = int(self.var_size.get())
        try: _c = Lire('{}\\DS config\\WG Symbols.ini'.format(getcwd())).assigne()
        except: _c = self.var_gras.get()
        try: _d = Lire('{}\\DS config\\SIG Symbols.ini'.format(getcwd())).assigne()
        except: _d = self.var_italic.get()
        try: _e = Lire('{}\\DS config\\ULG Symbols.ini'.format(getcwd())).assigne()
        except: _e = self.var_soul
        try: _f = Lire('{}\\DS Config\\OSG Symbols.ini'.format(getcwd())).assigne()
        except: _f = self.var_over
        self.style.configure('TEntry', font='%s %s' % (_a, _b))
        for ww in self.pal_b:
            ww.config(font=Font(family=_a, size=_b, weight=_c, slant=_d, underline=_e, overstrike=_f), fg=_g, bg=_h)
            ActiveLeave(ww)

        #################################################
        #                                                                                                                             #
        self.master.mainloop()  #                                                                     #
        #                                                                                                                               #
        #################################################
        
    def f_(self):
            self.f = self.entr_caract.get()
            self.master.after(50, self.f_)
        
    def copie(self, event=None):
        self.master.clipboard_clear()
        self.master.clipboard_append(str(self.pal_b[int(self.var.get()) - 1].cget('text')))

    def appliquer(self):
        a = str(self.comb_pol.get())
        if not a in POLICE:
            showwarning('Warning !', 'The font "%s" is not in our directory. The value "TkDefaultFont" may be assigned.' % self.comb_pol.get())
            self.var_pol.set('TkDefaultFont')
            a = self.var_pol.get()
        b = self.var_size.get()
        c = self.var_gras.get()
        d = self.var_italic.get()
        e = self.var_soul
        f = self.var_over
        g = self.fg_
        h = self.bg_
        self.style.configure('TEntry', font='%s %s' % (a, b))
        for ww in self.pal_b:
            ww.config(font=Font(family=a, size=b, weight=c, slant=d, underline=e, overstrike=f), fg=g, bg=h)
            ActiveLeave(ww)

        
    def ch_pol(self, event=None):
        a = str(self.comb_pol.get())
        self.style.configure('TEntry', font='%s %s' % (a, int(self.var_size.get())))
        for ww in self.pal_b:
            ww.config(font='%s %s' % (a, int(self.var_size.get())))
        Ecrire('{}\\DS config\\PFG Symbols.ini'.format(getcwd()), a)
        Ecrire('{}\\DS config\\SG Symbols.ini'.format(getcwd()), int(self.var_size.get()))

    def gras(self):
        a = self.var_gras.get()
        b = str(self.comb_pol.get())
        c = int(self.var_size.get())
        d = self.var_italic.get()
        e = self.var_soul
        f = self.var_over
        if a == 'bold':
            self.var_gras.set('normal')
            self.b_gras.deselect()
        elif a == 'normal':
            self.var_gras.set('bold')
            self.b_gras.select()
        for ww in self.pal_b:
                ww.config(font=Font(family=b, size=c, weight=self.var_gras.get(), slant=d, underline=e, overstrike=f))
        Ecrire('{}\\DS config\\WG Symbols.ini'.format(getcwd()), a)

    def italic(self):
        a = self.var_gras.get()
        b = str(self.comb_pol.get())
        c = int(self.var_size.get())
        d = self.var_italic.get()
        e = self.var_soul
        f = self.var_over
        if d == 'italic':
            self.var_italic.set('roman')
            self.b_italic.deselect()
        elif d == 'roman':
            self.var_italic.set('italic')
            self.b_italic.select()
        for ww in self.pal_b:
                ww.config(font=Font(family=b, size=c, weight=a, slant=self.var_italic.get(), underline=e, overstrike=f))
        Ecrire('{}\\DS config\\SIG Symbols.ini'.format(getcwd()), d)

    def soul(self):
        a = self.var_gras.get()
        b = str(self.comb_pol.get())
        c = int(self.var_size.get())
        d = self.var_italic.get()
        e = self.var_soul
        f = self.var_over
        if e is True:
            self.var_soul = False
            self.b_soul.deselect()
        elif e is False:
            self.var_soul = True
            self.b_soul.select()
        for ww in self.pal_b:
                ww.config(font=Font(family=b, size=c, weight=a, slant=d, underline=self.var_soul, overstrike=f))
        Ecrire('{}\\DS config\\ULG Symbols.ini'.format(getcwd()), e)

    def over(self):
        a = self.var_gras.get()
        b = str(self.comb_pol.get())
        c = int(self.var_size.get())
        d = self.var_italic.get()
        e = self.var_soul
        f = self.var_over
        if f is True:
            self.var_over = False
            self.b_over.deselect()
        elif f is False:
            self.var_over = True
            self.b_over.select()
        for ww in self.pal_b:
                ww.config(font=Font(family=b, size=c, weight=a, slant=d, underline=e, overstrike=self.var_over))
        Ecrire('{}\\DS config\\OSG Symbols.ini'.format(getcwd()), f)

    def coul_fg(self):
        a = Couleur().assigne()
        if a:
            self.fg_ = a
            for ww in self.pal_b:
                ww.config(fg=a)
                ActiveLeave(ww)
        Ecrire('{}\\DS config\\FGG Symbols.ini'.format(getcwd()), a)

    def coul_bg(self):
        a = Couleur().assigne()
        if a:
            self.bg_ = a
            for ww in self.pal_b:
                ww.config(bg=a)
                ActiveLeave(ww)
        Ecrire('{}\\DS config\\BGG Symbols.ini'.format(getcwd()), a)
                
    def ch_caract_spn(self, event=None):
        try:
            self.var_char.set(chr(int(str(eval(self.var_caract.get())))))
            a = int(str(eval(self.var_caract.get())))
            if a < 0:
                a = -a
            for ww in self.pal_index:
                if ww[0] <= a <= ww[1]:
                    self.lb_gbchr.select_set(self.pal_index.index(ww))
                    self.lb_gbchr.see(self.pal_index.index(ww))
                    break
            if a < 425:
                self.var.set(a + 1)
            else:
                self.var.set(a % 424 + 1)
            self.var_caract.set(int(str(eval(self.var.get()))) - 1)
            
            b = list(range(ww[0], ww[1] + 1))
            for ww in self.pal_b:
                ww.config(text=chr(int(b[self.pal_b.index(ww)])), command=lambda arg=ww: self.insert_chr(chr(int(b[self.pal_b.index(arg)]))))
            
        except:
            print(None, False)
            
    def selection(self, event=None):
        a = eval(str(self.lb_gbchr.curselection()[0]))
        ww = self.pal_index[a]
        b = list(range(ww[0], ww[1] + 1))
            
        for ww in self.pal_b:
                ww.config(text=chr(int(b[self.pal_b.index(ww)])), command=lambda arg=ww: self.insert_chr(chr(int(b[self.pal_b.index(arg)]))))

    def insert_chr(self, chr_):
            self.entr_caract.delete(0, END)
            self.entr_caract.insert(0, chr_)

    def rest_index(self, event=None):
        self.var_char.set(chr(0))
        self.var_caract.set(0)
        self.var.set(1)
        self.lb_gbchr.select_set(0)
        self.lb_gbchr.see(0)

    def rest_pol(self, event=None):
        self.var_pol.set('TkDefaultFont')
        for ww in self.pal_b:
            ww.config(font='TkDefaultFont')
        Ecrire('{}\\DS config\\PFG Symbols.ini'.format(getcwd()), 'TkDefaultFont')

    def rest_size(self, event=None):
        self.var_size.set(9)
        for ww in self.pal_b:
            ww. config(font=Font(size=9, family='TkDefaultFont'))
        Ecrire('{}\\DS config\\SG Symbols.ini'.format(getcwd()), '9')

    def rest_text(self, event=None):
        self.var_gras.set('normal')
        self.b_gras.deselect()
        self.var_italic.set('roman')
        self.b_italic.deselect()
        self.var_soul = False
        self.b_soul.deselect()
        self.var_over = False
        self.b_over.deselect()
        for ww in self.pal_b:
            ww.config(font=Font(weight='normal', slant='roman', underline=False, overstrike=False, size=9, family='TkDefaultFont'))
        Ecrire('{}\\DS config\\WG Symbols.ini'.format(getcwd()), 'normal')
        Ecrire('{}\\DS config\\SIG Symbols.ini'.format(getcwd()), 'roman')
        Ecrire('{}\\DS config\\ULG Symbols.ini'.format(getcwd()), False)
        Ecrire('{}\\DS config\\OSG Symbols.ini'.format(getcwd()), False)
        
    def rest_bg(self, event=None):
        self.bg_ = '#777777'
        for ww in self.pal_b:
            ww.config(bg=self.bg_)
            ActiveLeave(ww)
        Ecrire('{}\\DS config\\BGG Symbols.ini'.format(getcwd()), '#777777')

    def rest_fg(self, event=None):
        self.fg_ = 'SystemWindowText'
        for ww in self.pal_b:
            ww.config(fg=self.fg_)
            ActiveLeave(ww)
        Ecrire('{}\\DS config\\FGG Symbols.ini'.format(getcwd()), 'SystemWindowText')

    def restart(self, event=None):
        self.rest_index()
        self.rest_pol()
        self.rest_size()
        self.rest_text()
        self.rest_bg()
        self.rest_fg()
        for ww in self.pal_b:
                ww.config(text=chr(int(self.pal_b.index(ww))), command=lambda arg=ww: self.insert_chr(chr(int(self.pal_b.index(arg)))),)
        Ecrire('{}\\DS config\\PFG Symbols.ini'.format(getcwd()), 'TkDefaultFont')
        Ecrire('{}\\DS config\\SG Symbols.ini'.format(getcwd()), '9')
        Ecrire('{}\\DS config\\WG Symbols.ini'.format(getcwd()), 'normal')
        Ecrire('{}\\DS config\\SIG Symbols.ini'.format(getcwd()), 'roman')
        Ecrire('{}\\DS config\\ULG Symbols.ini'.format(getcwd()), False)
        Ecrire('{}\\DS config\\OSG Symbols.ini'.format(getcwd()), False)
        Ecrire('{}\\DS config\\BGG Symbols.ini'.format(getcwd()), '#777777')
        Ecrire('{}\\DS config\\FGG Symbols.ini'.format(getcwd()), 'SystemWindowText')

    def quitter(self, event=None):
        s = ttk.Style()
        s.theme_use(self.stl)
        if self.master_root:
                self.master_root.wm_attributes('-disabled', False)
        if self.wtexte:
            self.master.destroy()
        else:
            a = askyesno('Closing', 'Are you sure you want to close ?')
            if a is True:
                self.master.destroy()
            elif a is False:
                pass

    def bouger(self):
                a = self.pal1_[randrange(len(self.pal1_))]
                b = randrange(111111, 999999)
                self.can1.itemconfigure(a, font='None %s' % randrange(5, 20), fill=f'#{b}')
                if self.ver is True:
                    self.can1.after(4, self.bouger)

    def about(self):
        if self.ver is False:
            self.ver = True
            self.top1 = Toplevel(self.master)
            self.top1.title('Software Information')
            self.top1.protocol("WM_DELETE_WINDOW", self.t1)
            self.top1.wm_attributes('-toolwindow', True)
            self.master.wm_attributes('-disabled', True)
            self.top1.wm_attributes('-topmost', True)
            self.top1.transient(self.master)
            Assign(self.top1, self.t1, ['FocusOut'])
            self.can1 = Canvas(self.top1, width=500, height=120)
            self.can1.grid(row=1, column=1)
            self.pal1_ = []
            for ww in range(150):
                x = randrange(250, 501)
                y = randrange(121)
                s = randrange(360)
                coul = randrange(111111, 999999)
                self.pal1_.append(self.can1.create_text(x, y, angle=s, fill='#%s' % coul, text=chr(randrange(13175))))
            frame = ttk.Frame(self.top1, width=90, height=90)
            s = ttk.Style(self.top1)
            s.configure('TFrame', background='orange')
            frame.place(x=0, y=0)
            lab = ttk.Label(frame, text='''- Title: Symbols
- Version: 1.3.2
- Release date: November 22 2021''',
justify=LEFT, wraplength=300, width=45)
            lab.grid(row=1, column=1)

            self.top1.resizable(False, False)
            self.bouger()
            self.top1.mainloop()
            
    def t1(self, event=None):
        self.ver = False
        self.top1.destroy()
        self.master.wm_attributes('-disabled', False)

    def t2(self, event=None):
        self.car = False
        self.top2.destroy()

    def t4(self, event=None):
        self.ver_sc = False
        self.top4.destroy()
        self.master.wm_attributes('-disabled', False)
        self.top2.wm_attributes('-disabled', False)
        
    def save(self, event=None):
        a = asksaveasfilename(parent=self.master, defaultextension='*.txt', filetypes=[('All types', '*.*'), ('Normal text file', '*.txt'), ('Hyper Text Markup Language file', '*.html; *.htm; *.shtml; *.shtm; *.xhtml; *.xht; *.hta'),
                                                                                         ('MS ini file', '*.ini; *.inf; *.url; *.wer'), ('Lua source', '*.lua'), ('Batch file', '*.bat; *.cmd; *.nt'), ('Python file', '*.py; *.pyw'),
                                                                                         ('eXtensible Markup Language', '*.doc; *.docx; *.pdf; *.wps; *.wpt; *.dot; *.rft; *.txt; *.dotx')])
        if a:
            f = open(a, 'w')
            f.write(self.f)
            f.close()
            
    def inserer(self):
        a = self.wtexte.index(INSERT)
        self.wtexte.insert(a, str(self.pal_b[int(self.var.get()) - 1].cget('text')))
        self.quitter
        
    def insert(self, event=None):
        if self.ver_insert is False:
            self.ver_insert = True
            if self.twtexte == 'ENTRY':
                self.insert_entr()
            elif self.twtexte == 'TEXT':
                self.insert_txt()
            self.master.wm_attributes('-disabled', True)
        
    def sauv_chr2(self):
        x1 = self.entr_sc1.get()
        x2 = self.entr_sc3.get()
        y1 = self.entr_sc2.get()
        y2 = self.entr_sc4.get()
        self.pp1_ = list((x1, y1, x2, y2))
        a = 0
        for ww in self.pp1_:
            try:
                eval(ww)
                a += 1
            except:
                showerror('error', '%s is not a number. \ nReverify your value.' % ww, parent=self.top4)
                break
        if a == 4:
            self.ok1()

    def copie_chr(self):
        a = self.text_chr.get('0.0', END)
        self.master.clipboard_clear()
        self.master.clipboard_append(str(a))

        
    def sauv_chr(self):
        a = self.text_chr.get('0.0', END)
        b = asksaveasfilename(parent=self.text_chr, filetypes=[('Text Files', '*.txt')])
        if len(b) > 3:
            Ecrire(b, 'w')
        else: pass
        
    def caract_only(self):
        self.text_chr['stat'] = 'normal'
        self.text_chr.delete(0.0, END)
        a = 0; b = 0
        while True:
                    try:
                        if a == 9:
                            a = 0
                            self.text_chr.insert(END, '\n')
                        self.text_chr.insert(END, '%s    ' % str(chr(b)))
                        b += 1
                        a += 1
                    except:
                        self.text_chr['stat'] = 'disabled'
                        break

    def norm_comb(self):
        self.text_chr['stat'] = 'normal'
        self.text_chr.delete(0.0, END)
        a = 0; b = 0
        while True:
                    try:
                        if a == 9:
                            a = 0
                            self.text_chr.insert(END, '\n')
                        self.text_chr.insert(END, '%s: %s     ' % (chr(b), b))
                        b += 1
                        a += 1
                    except:
                        self.text_chr['stat'] = 'disabled'
                        break

    def valeur_first(self):
        self.text_chr['stat'] = 'normal'
        self.text_chr.delete(0.0, END)
        a = 0; b = 0
        while True:
                    try:
                        if a == 9:
                            a = 0
                            self.text_chr.insert(END, '\n')
                        self.text_chr.insert(END, '%s: %s     ' % (b, chr(b)))
                        b += 1
                        a += 1
                    except:
                        self.text_chr['stat'] = 'disabled'
                        break
    
    def caract(self):
        if self.car is False:
            self.car = True
            rt = 1112111
            while True:
                try:
                    chr(rt)
                    rt += 1
                except:
                    break
            a = askyesno('Warning', 'Attention, all characters will be displayed. \nContinue to the very high number ({}); the computer may be slow. \n\nDo you really want to continue the operation?'.format(rt),
                       icon='warning')
            if a is True:
                self.top2 = Toplevel(self.master)
                self.top2.title('All characters with their values')
                self.top2.protocol('WM_DELETE_WINDOW', self.t2)
                if self.icontype == 'photo':
                    self.top2.iconphoto(False, PhotoImage(file=self.icon))
                elif self.icontype == 'bitmap':
                    self.top2.iconbitmap(self.icon)
                self.var_ch_forme = StringVar(value=0)
                ttk.Radiobutton(self.top2, text='Combined normals', value=0, variable=self.var_ch_forme, command=self.norm_comb).grid(row=1, column=1, sticky=EW)
                ttk.Radiobutton(self.top2, text='Characters only', value=1, variable=self.var_ch_forme, command=self.caract_only).grid(row=1, column=2, sticky=EW)
                ttk.Radiobutton(self.top2, text='Forward values', value=2, variable=self.var_ch_forme, command=self.valeur_first).grid(row=1, column=3, sticky=EW)
                self.text_chr = ScrolledText(self.top2, width=135, height=35)
                self.text_chr.grid(row=2, column=1, columnspan=3, sticky=EW)
                ttk.Button(self.top2, text='Copy characters...     ', command=self.copie_chr).grid(row=3, column=1)
                ttk.Button(self.top2, text='Save as file...     ✔', command=self.sauv_chr).grid(row=3, column=2)
                a = 0; b = 0
                while True:
                    try:
                        if a == 9:
                            a = 0
                            self.text_chr.insert(END, '\n')
                        self.text_chr.insert(END, '%s: %s     ' % (chr(b), b))
                        b += 1
                        a += 1
                    except:
                        break
                self.text_chr.config(stat='disabled')
                self.top2.resizable(False, False)


if __name__ == '__main__':
    Chr()

