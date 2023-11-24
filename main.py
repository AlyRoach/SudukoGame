from tkinter import *
from tkinter import messagebox
import random
from stack import Stack

class BorderedFrame(Frame):
    def __init__(self, root = None, color = "black", thickness = 1, **kargs):
        Frame.__init__(self, root, highlightbackground = color, highlightthickness = thickness, **kargs) 
        self.color = color
        self.__root = root

    def setColor(self,value = "black"):
        if value in ["red","green","blue","black","white"] and self.color != value:
            self.color = value
            self.config(highlightbackground = self.color)

    def setThickness(self,value):
        if isinstance(value,int) and value >= 0 and value <= 5:
            self.config(highlightthickness = value)

class GridButton(Button):
    def __init__(self, root = None, immutable = False, **kargs):
        Button.__init__(self,root,relief = FLAT, bg = "white", width = 2, height = 0, **kargs)
        self.__root = root
        self.pack(ipadx = 5, ipady = 5)
        self.setMutability(immutable)
        self.setContent('0')

    def setMutability(self,value = False):
        if isinstance(value,bool):
            if value:
                self.config(state = DISABLED, bg = "gray85")
            else:
                self.config(state = NORMAL, bg = "white")

    def setContent(self,value):
        if isinstance(value,str) and len(value) == 1 and value.isdigit():
            if value == '0':
                self.config(text = "  ")
            else:
                self.config(text = value)

    def getRoot(self):
        return self.__root

class ColorButton(Button):
    def __init__(self, root = None, **kargs):
        Button.__init__(self,root, bg = "gray80", width = 2, height = 0, **kargs)
        self.__root = root

    """changes the background color of the button"""    
    def setColor(self,value = False):
        if isinstance(value,bool):
            self.config(bg = ("gray80","white")[value])

class Game(Tk):           
    def __init__(self):
        Tk.__init__(self)
        self.configure(background = "white")
        self.title("Sudoku Game")
        self.otherFrame = Frame(self, bg = "white")
        self.digitBtns = [ColorButton(self.otherFrame, text = str(i+1)) for i in range(9)]
        self.undoBtn = Button(self.otherFrame, text = 'Undo', width = 2, height = 0, bg = "gray80")
        self.restartBtn = Button(self.otherFrame, text = 'Restart', width = 2, height = 0, bg = "gray80")
        self.eraseBtn = Button(self.otherFrame, text = 'Erase', width = 2, height = 0, bg = "gray80")
        self.newBtn = Button(self.otherFrame, text = 'New', width = 2, height = 0, bg = "gray80")
        self.mainFrame = Frame(self, height = 360, width = 360, highlightthickness = 2)
        self.boxFrames = [BorderedFrame(self.mainFrame, height = 120, width = 120, thickness = 2) for i in range(9)]
        self.cellFrames = [BorderedFrame(self.boxFrames[((i//27)*3)+((i%9)//3)],height = 40, width = 40) for i in range(81)]
        self.gridBtns = [GridButton(self.cellFrames[i]) for i in range(81)]
        self.mainFrame.pack()
        self.otherFrame.pack(pady = 30)
        self.gameNumber = None
        self.stack = [Stack(),Stack()]
        self.isErase = False

        """render boxes in the main grid frame"""
        for i in range(3):
            for j in range(3):
                self.boxFrames[3 * i + j].grid(row = i, column = j)
        """render cells in the box frames"""
        for i in range(9):
            for j in range(9):
                self.cellFrames[9*i+j].grid(row = i, column = (j % 3))
                self.gridBtns[9*i+j].config(command = lambda i = i, j = j: self.PopulateCell(i,j))

        """render digit buttons and undo button in the other frame"""
        for i in range(9):
            self.digitBtns[i].grid(row = 0, column = i, ipadx = 5, ipady = 5, padx = 2)
            self.digitBtns[i].config(command = lambda i = i: self.SelectDigit(i))
        self.undoBtn.grid(row = 1, column = 4, ipadx = 5, ipady = 5, pady = 3)
        self.undoBtn.config(command = lambda: self.Undo())
        self.eraseBtn.grid(row = 1, column = 5, ipadx = 5, ipady = 5, pady = 3)
        self.eraseBtn.config(command = lambda: self.EraseCell())
        self.restartBtn.grid(row = 1, column = 6, ipadx = 5, ipady = 5, pady = 3)
        self.restartBtn.config(command = lambda: self.Restart())
        self.newBtn.grid(row = 1, column = 7, ipadx = 5, ipady = 5, pady = 3)
        self.newBtn.config(command = lambda: self.New())
        
        self.geometry("600x600")
        """makes the size of the app fixed"""
        self.resizable(0,0)
        self.Initialize()

    def Initialize(self):
        self.data = ["0" for i in range(81)]
        self.selected = 0
        self.Display('d',0)

        puzzle = self.SelectPuzzle()

        for i in range(81):
            if puzzle[1][i] == '1':
                self.data[i] = puzzle[0][i]
                self.gridBtns[i].setMutability(True)
        self.Display('g',0)

    def Display(self,cat,value):
        for i in range(81):
            self.gridBtns[i].getRoot().setColor()
        if cat == 'd':
            self.digitBtns[self.selected].setColor()
            self.selected = value
            self.digitBtns[self.selected].setColor(True)
        elif cat == 'g':
            for i in range(81):
                self.gridBtns[i].setContent(self.data[i])
                self.gridBtns[i].getRoot().setThickness(1)
        if self.HasWon():
            messagebox.showinfo("Congratulations", "You Win!")
            self.New()
            return

    def SelectPuzzle(self):
        solves =                       ["829143526978168257149319783456282619534737465951743628519326874248957136763418259",
        "152489376739256841468371295387124659591763428246895713914637582625948137873512964",
        "123678945584239761967145328372461589691583274458792613836924157219857436745316892",
        "581672439792843651364591782438957216256184973179326845845219367913768524627435198",
        "276314958854962713913875264468127395597438621132596487325789146641253879789641532"
        ]
        givens = [
        "000110101110010010110001100110100010001101100010001011001100011010010011101011000",
        "100111001110000010000001111001110100100101001001011100111100000010000011100111001",
        "010101000110001100000010000110000100100000001001000011000010000001100011000101010",
        "000100100100001100000011010000000000010110001000101011010100010101000000010000100",
        "100100000101011001011100100000010110101000111011001000010001110101110101000001001"
        ]
        if self.gameNumber is not None:
          while True:
            number = random.randint(0,4)
            if self.gameNumber != number:
              self.gameNumber = number
              break
          return solves[number], givens[number]
        
        self.gameNumber = random.randint(0, 4)
        solved = solves[self.gameNumber]
        given = givens[self.gameNumber]

        return (solved, given)

    def HasWon(self):
        for i in range(81):
            if self.data[i] == '0':
              return False
        return True

    def SelectDigit(self,value):
        self.Display('d', value)
      
    def PopulateCell(self,row,col):
        if self.gridBtns[row*9+col].cget('state') == 'disabled':
            return
        if self.isErase:
          self.stack[0].push(row * 9 + col)
          self.stack[1].push(self.data[row*9+col])
          self.data[row*9+col] = str(self.selected + 1) 
          self.EraseCell()
          self.Display('g',0)
        else:
          if not self.IsValidRow(row) or not self.IsValidColumn(col) or not self.IsValidBox(row,col):
            return
          self.stack[0].push(row * 9 + col)
          self.stack[1].push(self.data[row*9+col])
          self.data[row*9+col] = str(self.selected + 1) 
          self.Display('g',0)

    def IsValidRow(self,row):
        for i in range(9):
          if self.data[row*9+i] == str(self.selected + 1):
            self.gridBtns[row*9+i].getRoot().setColor('red')
            self.gridBtns[row*9+i].getRoot().setThickness(3)
            return False
        return True

    def IsValidColumn(self,col):
        for i in range(9):
          if self.data[i*9+col] == str(self.selected + 1):
            self.gridBtns[i*9+col].getRoot().setColor('red')
            self.gridBtns[i*9+col].getRoot().setThickness(3)
            return False
        return True

    def IsValidBox(self,row,col):
        for i in range(3):
          for j in range(3):
            index = 9 * ((row // 3) * 3 + i) + ((col // 3) * 3 + j)
            if self.data[index] == str(self.selected + 1):
              self.gridBtns[index].getRoot().setColor('red')
              self.gridBtns[index].getRoot().setThickness(3)
              return False
        return True

    def Undo(self):
        if self.stack[0].isEmpty() or self.stack[1].isEmpty():
            return
        index = self.stack[0].pop()
        value = self.stack[1].pop()
        self.data[index] = value
        self.Display('g',0)

    def Restart(self):
        self.stack = [Stack(),Stack()]
        for i in range(81):
            if self.gridBtns[i].cget('state') == 'normal':
              self.data[i] = '0'
        self.Display('d',0)
        self.Display('g',0)

    def New(self):
        self.stack = [Stack(),Stack()]
        self.data = ["0" for i in range(81)]
        self.selected = 0
        self.Display('d',0)

        puzzle = self.SelectPuzzle()

        for i in range(81):
            if puzzle[1][i] == '1':
                self.data[i] = puzzle[0][i]
                self.gridBtns[i].setMutability(True)
            else:
                self.gridBtns[i].setMutability(False)
        self.Display('g',0)

    def EraseCell(self):
      self.isErase = not self.isErase
      if self.isErase:
        self.eraseBtn.config(bg='green')
        for i in range(9):
          self.digitBtns[i].config(state='disabled')
        self.restartBtn.config(state='disabled')
        self.newBtn.config(state='disabled')
        self.undoBtn.config(state='disabled')
      else:
        self.eraseBtn.config(bg='gray80')
        for i in range(9):
          self.digitBtns[i].config(state='normal')
        self.restartBtn.config(state='normal')
        self.newBtn.config(state='normal')
        self.undoBtn.config(state='normal')


if __name__ == '__main__':
    app = Game()
    app.mainloop()
