"""
Python collaborate project
Madipoupou
16/07/2020
"""

import tkinter as tk
from random import randint

# CLASS DEFINITION
class FaceDom(object):
    """ Dice class """
    def __init__(self, can, val, pos, taille=70):
        self.can = can
        # Init the position of the dice and creating the square
        x, y, c = pos[0], pos[1], taille/2
        self.dice = can.create_rectangle(x-c, y-c, x+c, y+c, fill='ivory', width=2)
        d = taille / 3

        # Creating a list containing all the point of the dice (the addresses)
        self.pList= []

        # Creating a list of possible "shapes" of dices and selecting the current one
        pDispo = [
            ((0, 0),),
            ((-d, d), (d, -d)),
            ((-d, d), (0, 0), (d, -d)),
            ((-d, -d), (d, -d), (-d, d), (d, d)),
            ((-d, -d), (d, -d), (-d, d), (d, d), (0, 0)),
            ((-d, -d), (d, -d), (-d, d), (d, d), (0, d), (0, -d))
        ]
        disp = pDispo[val - 1]
        
        # Drawing the points
        for p in disp:
            self.cercle(x + p[0], y + p[1], taille/10, 'red')
    
    def cercle(self, x, y, r, coul):
        # Drawing the points and adding them to the list of addresses
        self.pList.append(self.can.create_oval(x-r, y-r, x+r, y+r, fill=coul))
    
    def remove_dice(self):
        # Cleaning the dice by removing its points
        for p in self.pList:
            self.can.delete(p)
        self.can.delete(self.dice)
    
    def lock(self):
        self.can.itemconfig(self.dice, fill='grey')
    
    def unlock(self):
        self.can.itemconfig(self.dice, fill='ivory')

class Projet(tk.Frame):
    def __init__(self, larg, haut):
        # Canvas initialization
        tk.Frame.__init__(self)
        self.larg, self.haut = larg, haut
        self.can = tk.Canvas(self, bg='dark green', width=larg, height=haut)
        self.can.pack(padx=5, pady=5)
        self.can.bind('<Button-1>', self.on_click)
        
        # Creating the canvas buttons
        bList = [
            ("ROLL", self.boutA), ("CLEAN", self.boutB),
            ("EXIT", self.boutQuit)
        ]
        for b in bList[::-1]:
            tk.Button(self, text=b[0], command=b[1]).pack(side=tk.RIGHT, padx=10, pady=10)
        self.pack(padx=10, pady=10)

        # Initializing dices list
        self.dices = []
    
    def boutA(self):
        """ Create six dices each one having a random value """
        temp = self.dices
        if (self.dices != []):
            self.boutB()
        dices_shapes = [
            [randint(1, 6), (100, 200), 100],
            [randint(1, 6), (300, 200), 100],
            [randint(1, 6), (500, 200), 100],
            [randint(1, 6), (100, 400), 100],
            [randint(1, 6), (300, 400), 100],
            [randint(1, 6), (500, 400), 100]
        ]
        for i in range(len(temp)):
            if (temp[i]['locked']):
                dices_shapes[i][0] = temp[i]['val']
        for i in range(len(dices_shapes)):
            dice = dices_shapes[i]
            self.dices.append({
                'dice': FaceDom(self.can, dice[0], dice[1], dice[2]),
                'coord': dice[1],
                'size': dice[2],
                'val': dice[0],
                'locked': False
            })
            if (temp != [] and temp[i]['locked']):
                self.dices[i]['locked'] = True
                self.dices[i]['dice'].lock()
        del temp

    def boutB(self):
        # Delete all the points on the d3 dice
        for dice in self.dices:
            dice['dice'].remove_dice()
        self.dices = []
    
    def boutQuit(self):
        self.master.destroy()
    
    def on_click(self, event):
        x = event.x
        y = event.y
        for dice in self.dices:
            xmin, xmax = dice['coord'][0] - dice['size'] / 2, dice['coord'][0] + dice['size'] / 2
            ymin, ymax = dice['coord'][1] - dice['size'] / 2, dice['coord'][1] + dice['size'] / 2
            if (x >= xmin and x <= xmax and y >= ymin and y <= ymax):
                if (dice['locked']):
                    dice['locked'] = False
                    dice['dice'].unlock()
                else:
                    dice['locked'] = True
                    dice['dice'].lock()
                break

# MAIN PROGRAM
if (__name__ == '__main__'):
    root= tk.Tk()
    root.resizable(False, False)
    root.title('Yathzee Dices')
    root.geometry('+0+0')
    root.bind('<Escape>', lambda event: root.destroy())
    pro = Projet(600, 600)
    pro.mainloop()
