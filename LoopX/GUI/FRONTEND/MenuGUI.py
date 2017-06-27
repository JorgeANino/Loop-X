# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 00:28:40 2017

@author: Jorge Alberto Niño Cabal
version: 0.1
"""

from Lib import *
import StockWindowsGUI
import ImageLabel
import appJar

class MenuGUI(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.master = master
        master.title("Loop X")
        #Next line makes window not resizable
        self.master.minsize(width=350,height=550)
        self.master.maxsize(width=350, height=550)
        self.master.resizable(False,False)
        self.master.iconbitmap("Images\\fib.ico")
        self.master.configure(background="white")
        self.grid()
        self.create_Widgets()
        self.runSp500 = False


    def create_Widgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.columnconfigure(0, weight=1)

        self.menubar = tk.Menu(self.master)
        self.menu= tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Menu",menu=self.menu)
        self.menu.add_command(label="Analyze Stock(s)",command=self.open_stock_window)
        self.menu.add_command(label="Compare Stocks",command=self.open_stock_compare_window)
        self.menu.add_separator()
        self.menu.add_command(label="Exit Program", command=self.master.destroy)

        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call(self.master,"config","-menu",self.menubar)

        self.img = ImageLabel.ImageLabel(self.master)
        self.img.config(bg="white")
        self.img.grid(column=0, row=0)
        self.img.load("Images\\fibgif.gif")

        self.menuFont = tkFont.Font(family="Showcard Gothic",weight="bold",size=40,slant = "italic")
        self.menuLabel = tk.Label(self.master, text=" LOOP X ",font=self.menuFont,bg="white")
        self.menuLabel.grid(column=0,row=1)
        self.menuLabel.config(width=self.master.winfo_width())

        self.signatureFont = tkFont.Font(family="Abadi MT Condensed Light",weight="bold", size=10,slant="italic")
        self.signatureLabel = tk.Label(self.master, text="Author: Jorge Alberto Niño Cabal", font=self.signatureFont,bg="white")
        self.signatureLabel.grid(column=0, row=3)
        self.signatureLabel.config(width=self.master.winfo_width())

        self.optionsFont = tkFont.Font(family="Cooper Plate Ghotic Bold",weight="bold", size=10)
        self.optionsLabel = tk.Label(self.master, text="Welcome. What would you like to do?",font=self.optionsFont,bg="white")
        self.optionsLabel.grid(column=0, row=4)
        self.optionsLabel.config(width=self.master.winfo_width())

        self.analyzeStock = tk.Button(self.master, text="Analyze Stock(s)", command=self.open_stock_window, bg="white")
        self.analyzeStock.grid(column=0,row=5)
        self.analyzeStock.config(width=self.master.winfo_width(),height=3)

        self.compareStock = tk.Button(self.master, text="Compare Stocks",command=self.open_stock_compare_window, bg="white")
        self.compareStock.grid(column=0, row=6)
        self.compareStock.config(width=self.master.winfo_width(),height=3)
        """
        THIS PROGRAM BUTTON AND FUNCTION IS CURRENTLY UNDER DEVELOPMENT
        self.sp500Stock = tk.Button(self.master, text="Analyze S&P500", command=self.open_sp500_window, bg="white")
        self.sp500Stock.grid(column=0, row=7)
        self.sp500Stock.config(width=self.master.winfo_width())
        """
        self.close_buttonA = tk.Button(self.master, text="Exit Program", command=self.master.destroy, bg="white")
        self.close_buttonA.grid(column=0, row=7)
        self.close_buttonA.config(width=self.master.winfo_width(),height=3)



    def open_stock_window(self):
        self.stockWindow = StockWindowsGUI.StockGUI(self.master)

    def open_stock_compare_window(self):
        self.stockCWindows = StockWindowsGUI.StockCompareGUI(self.master)
    """
    THIS PROGRAM FUNCTION IS CURRENTLY UNDER DEVELOPMENT
    def open_sp500_window(self):
        self.sp500window = StockWindowsGUI.Sp500GUI(self.master)
    """




