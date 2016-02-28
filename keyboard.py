#!/usr/bin/python
# -*- coding: utf-8 -*-

import curses, threading, time, subprocess
import locale

class Keyboard(object):

    class Sweep(threading.Thread):
        def __init__(self,board,*args,**kwargs):
            self.board=board
            self.now=()
            self.swp='row'
            self.pharses=7
            self.is_phrases=False
            super(Keyboard.Sweep,self).__init__(*args,**kwargs)

        def run(self):
            self.col_last=-1
            self.row_last=-1
            #self.board.lay_keys()
            time.sleep(0.5)
            while True:
                self.is_phrases=False
                if self.swp=='row': self.row_sweep()
                elif self.swp=='col': self.col_sweep()
                
        def row_sweep(self):
            for i in range(len(self.board.layout)):
                if i>self.pharses and self.is_phrases==False:
                    break
                self.now=(i,)
                if self.row_last!=-1:
                    self.board.scr.addstr(self.row_last,0,'    ')
                self.board.scr.addstr(i+6,0,'--->')
                self.board.scr.refresh()
                self.row_last=i+6
                time.sleep(0.75)
                if i==0: time.sleep(0.25)
                if Keyboard.blink_counter>0 and Keyboard.blink_counter<4:
                    if self.now==(self.pharses,):
                        Keyboard.blink_counter=0
                        self.is_phrases=True
                        continue
                    if self.row_last!=-1:
                        self.board.scr.addstr(self.row_last,0,'--->')
                    self.col_last=-1
                    self.swp='col'
                    break

        def col_sweep(self):
            self.swp='row'
            Keyboard.blink_counter=0
            row=self.now[0]+6
            rng=range(len(self.board.layout[row-6]))
            for i in rng:
                self.now=(row-6,i)
                if self.col_last!=-1:
                    self.board.scr.addch(row,(self.col_last+1)*8-1,' ')
                self.board.scr.addch(row,(i+1)*8-1,'>')
                self.board.scr.refresh()
                self.col_last=i
                time.sleep(1)
                if Keyboard.blink_counter>0 and Keyboard.blink_counter<4:
                    if self.col_last!=-1:
                        self.board.scr.addch(row,(self.col_last+1)*8-1,' ')
                    self.board.put_string(self.now[0],self.now[1])
                    Keyboard.blink_counter=0
                    break
                if i==rng[-1]:
                    if self.col_last!=-1:
                        self.board.scr.addch(row,(self.col_last+1)*8-1,' ')

    class Update(threading.Thread):
        def __init__(self,board,*args,**kwargs):
            self.board=board
            super(Keyboard.Update,self).__init__(*args,**kwargs)

        def run(self):
            while True:
                self.board.scr.move(2,0)
                if Keyboard.poor_signal==200:
                    self.board.scr.clrtoeol()
                    self.board.scr.addstr(2,0,"Headset not connected properly.")
                elif Keyboard.poor_signal==0:
                    self.board.scr.clrtoeol()
                    self.board.scr.addstr(2,0,"The signal is ok.")
                else:
                    self.board.scr.clrtoeol()
                    self.board.scr.addstr(2,0,"The signal is too poor: "+str(Keyboard.poor_signal))
                self.board.scr.refresh()
                time.sleep(0.25)

    def __init__(self,screen):
        self.scr=screen
        self.row=0
        self.col=0
        Keyboard.blink=False
        Keyboard.blink_counter=0
        Keyboard.poor_signal=0
        self.string=''
        self.deleted=False

        self.layout = [
            ['SPACE','SAY','BACK','CLEAR','SAVE'],
            ['A','B','C','D','E','F'],
            ['G','H','I','J','K','L'],
            ['M','N','O','P','Q','R'],
            ['S','T','U','V','W','X'],
            ['Y','Z','0','1','2','3'],
            ['4','5','6','7','8','9'],
            ['Phrases: '],
            ['HELLO',u'नमस्ते',u'धन्यबाद'],
            ['MY NAME IS '],
            ['HOW ARE YOU?'],
            ['NICE TO MEET YOU'],
            ['GOOD BYE'],
            ['GOOD MORNING'],
            ['GOOD AFTERNOON'],
            ['GOOD EVENING'],
        ]

        self.sweeper=self.Sweep(self)
        self.sweeper.daemon=True
        self.sweeper.start()

        self.val_update=self.Update(self)
        self.val_update.daemon=True
        self.val_update.start()

    def put_string(self,r,c):
        if r==0:
            if c==0: 
                self.string+=' '
            elif c==1:
                subprocess.call(["espeak",self.string])
                self.lay_keys()
                self.string=''
            elif c==2:
                self.string=self.string[:-1]
            elif c==3:
                self.lay_keys()
                self.string=''
            elif c==4:
                f=open('file.txt','a')
                f.write(self.string.encode('utf-8')+'\n')
                self.string=''
                f.close()
        else:
            self.string+=self.layout[r][c]
        self.scr.move(4,2)
        self.scr.clrtoeol()
        self.scr.addstr(4,2,self.string.encode('utf-8'))

    def lay_keys(self):
        string=''
        for row in self.layout:
            for col in row:
                string+='\t'+col
            string+='\n'

        self.scr.erase()
        self.scr.addstr(0,0,"Blink Speaker")
        self.scr.addstr(4,0,": ")
        self.scr.addstr(6,0,string.encode('utf-8'))
        self.scr.refresh()

    def select(self):
        Keyboard.blink_counter=2

def main(self,scr):
    k=Keyboard(scr)
    k.lay_keys()
    while True:
        c=scr.getch()
        if c==curses.KEY_RIGHT:
            k.select()

def start():
    locale.setlocale(locale.LC_ALL,"")
    stdscr=curses.initscr()
    curses.curs_set(0)
    curses.wrapper(main,stdscr)


if __name__=='__main__':
    try:
        start()
    except KeyboardInterrupt:
        print "interrupted"
