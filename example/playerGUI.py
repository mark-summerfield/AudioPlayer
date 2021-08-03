#!/usr/bin/env python3

import os
import platform
import tkinter
import tkinter.filedialog
import tkinter.messagebox

import audioplayer


def main():
    player = Player()
    root = tkinter.Tk()
    config_root(root)
    make_widgets(root, player)
    root.mainloop()


def config_root(root):
    root.title('Music Player')
    root.attributes('-topmost', True)
    root.resizable(False, False)
    root.attributes('-topmost', False)


def make_widgets(root, player):
    botframe = tkinter.Frame()
    botframe.pack(fill=tkinter.X, side=tkinter.TOP)
    namelabel = tkinter.Label(botframe, anchor=tkinter.W, font=LABELFONT)
    namelabel.pack(fill=tkinter.X, expand=1, side=tkinter.LEFT, padx=2)
    vollabel = tkinter.Label(botframe, text='100%', anchor=tkinter.E,
                             font=LABELFONT)
    vollabel.pack(side=tkinter.LEFT, padx=0)

    player.namelabel = namelabel
    player.vollabel = vollabel

    toolbar = tkinter.Frame(root)
    toolbar.pack(side=tkinter.TOP)
    tkinter.Button(toolbar, text=BUTTONS_GLYPH[0], font=BUTTONFONT,
                   width=2, command=player.load).pack(side=tkinter.LEFT)
    tkinter.Button(toolbar, text=BUTTONS_GLYPH[1], font=BUTTONFONT,
                   width=2, command=player.play).pack(side=tkinter.LEFT)
    tkinter.Button(toolbar, text=BUTTONS_GLYPH[2], font=BUTTONFONT,
                   width=2,
                   command=player.tooglepause).pack(side=tkinter.LEFT)
    tkinter.Button(toolbar, text=BUTTONS_GLYPH[3], font=BUTTONFONT,
                   width=2, command=player.stop).pack(side=tkinter.LEFT)

    volframe = tkinter.Frame(toolbar)
    volframe.pack(side=tkinter.LEFT, expand=1, fill=tkinter.BOTH)
    tkinter.Button(
        volframe, text='➕',
        command=lambda player=player: player.changevolume(10)).pack(
        side=tkinter.TOP, expand=1, fill=tkinter.BOTH)
    tkinter.Button(
        volframe, text='➖',
        command=lambda player=player: player.changevolume(-10)).pack(
        side=tkinter.TOP, expand=1, fill=tkinter.BOTH)


BUTTONFONT = (None, 30)
LABELFONT = (None, 8)
BUTTONS_GLYPH = (('⏏', '▶', '⏯', '⏹') if platform.system() == 'Windows' else
                 ('⏏️', '▶️', '⏯️', '⏹️'))


class Player:

    def __init__(self):
        self.vollabel = None
        self.namelabel = None
        self.paused = False
        self.player = None


    def load(self):
        fname = tkinter.filedialog.askopenfilename()
        if fname:
            self.player = audioplayer.AudioPlayer(fname)
            self.changevolume(0)  # update UI
            self.namelabel.config(
                text=os.path.basename(self.player.fullfilename))
            try:
                self.player.play()
            except Exception as err:
                tkinter.messagebox.showerror('Error', err)


    def tooglepause(self):
        if self.player is not None:
            if self.paused:
                self.player.resume()
            else:
                self.player.pause()
            self.paused = not self.paused


    def play(self):
        if self.player is not None:
            try:
                self.player.play()
            except Exception as err:
                tkinter.messagebox.showerror('Error', err)


    def stop(self):
        if self.player is not None:
            self.player.stop()


    def changevolume(self, delta):
        if self.player is not None:
            self.player.volume += delta
            self.vollabel.config(text='{}%'.format(self.player.volume))


if __name__ == '__main__':
    main()
