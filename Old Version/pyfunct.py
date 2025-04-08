from tkinter import Tk
from tkinter.font import families
from tkinter.colorchooser import askcolor
import pickle as pkl

class Lire(object):
    def __init__(self,fichier=None):
        f=open(fichier,'rb')
        self.t=''
        while True:
            try:
                self.t+=str(pkl.load(f))
            except:
                f.close()
                break
        self.assigne()
    def assigne(self):
        return self.t

class Ecrire(object):
    def __init__(self,fichier=None,info=None):
        f=open(fichier,'wb')
        pkl.dump(info,f)
        f.close()


class ActiveLeave(object):

    def __init__(self, widget, bg='blue', fg='dark grey', bordure=0, contour='navy blue', add=[]):
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


class Desassigne(object):

    def __init__(self, mil, touche=[], definit=None):
        self.m = mil
        self.d = definit
        self.t = touche
        for ww in self.t:
            self.m.unbind('<%s>' % ww)

    def modifie(self, mil=None, definit=None, touche=[]):
        if mil != None:
            self.m = mil
        if definit != None:
            self.d = definit
        if touche != []:
            self.t = touche
        for ww in self.t:
            self.m.unbind('<{}>'.format(ww))


class Couleur(object):

    def __init__(self, color='black'):
        self.coul = askcolor('black')[1]

    def assigne(self):
        return self.coul


CURSEURS = ['X_cursor', 'arrow', 'based_arrow_down', 'based_arrow_up', 'boat', 'bogosity',
          'bottom_left_corner', 'bottom_right_corner', 'bottom_side', 'bottom_tee', 'box_spiral',
          'center_ptr', 'circle', 'clock', 'coffee_mug', 'cross', 'cross_reverse', 'crosshair', 'diamond_cross',
          'dot', 'dotbox', 'double_arrow', 'draft_large', 'draft_small', 'draped_box', 'exchange', 'fleur', 'gobbler',
          'gumby', 'hand1', 'hand2', 'heart', 'icon', 'iron_cross', 'left_ptr', 'left_side', 'left_tee', 'leftbutton', 'll_angle',
          'lr_angle', 'man', 'middlebutton', 'mouse', 'pencil', 'pirate', 'plus', 'question_arrow', 'right_ptr', 'right_side',
          'right_tee', 'rightbutton', 'rtl_logo', 'sailboat', 'sb_down_arrow', 'sb_h_double_arrow', 'sb_left_arrow',
          'sb_right_arrow', 'sb_up_arrow', 'sb_v_double_arrow', 'shuttle', 'sizing', 'spider', 'spraycan', 'star', 'target',
          'tcross', 'top_left_arrow', 'top_left_corner', 'top_right_corner', 'top_side', 'top_tee', 'trek', 'ul_angle',
          'umbrella', 'ur_angle', 'watch', 'xterm']

fen = Tk()
P = list(families())
POLICE = []
POLICE.append('TkDefaultFont')

for ww in P:
    POLICE.append(ww)
fen.destroy()
del(fen)

