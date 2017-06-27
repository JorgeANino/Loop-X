# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 00:28:40 2017

@author: Jorge Alberto Niño Cabal
version: 0.1
"""

from Lib import *
class StockGUI():
    def __init__(self,master):
        self.master = master
        self.stockWindow = tk.Toplevel(self.master)
        self.stockWindow.title("Analyze Stock(s)")
        self.stockWindow.iconbitmap("Images\\fib.ico")
        self.stockWindow.configure(background="white")
        self.stockWindow.minsize(width=400, height=133)
        self.stockWindow.maxsize(width=400, height=133)
        self.stockWindow.resizable(False, False)
        self.createWidgets(self.stockWindow)

    def createWidgets(self,window):

        self.menubar = tk.Menu(self.stockWindow)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.menu)
        self.menu.add_command(label="Open New Window", command=self.open_new_window)
        self.menu.add_separator()
        self.menu.add_command(label="Close Window", command=self.stockWindow.destroy)
        try:
            self.stockWindow.config(menu=self.menubar)
        except AttributeError:
            self.stockWindow.tk.call(self.master, "config", "-menu", self.menubar)

        self.symbolText = tk.Entry(window)
        self.symbolText.grid(column=1, row=0)
        self.symbolLabel = tk.Label(window, text="Enter Stock symbol: ", bg="white")
        self.symbolLabel.grid(column=0, row=0)

        self.startText = tk.Entry(window)
        self.startText.grid(column=1, row=1)
        self.startLabel = tk.Label(window, text="Enter start date(format: 'YEAR-DAY-MONTH'): ", bg="white")
        self.startLabel.grid(column=0, row=1)

        self.endText = tk.Entry(window)
        self.endText.grid(column=1, row=2)
        self.endLabel = tk.Label(window, text="Enter end date(format: 'YEAR-DAY-MONTH'): ", bg="white")
        self.endLabel.grid(column=0, row=2)

        self.addStockB = tk.Button(window, text="Add Stock", command=self.add_Stock, bg="white")
        self.addStockB.grid(column=0, row=3, columnspan=2)
        self.addStockB.config(width=56)

        self.close_buttonB = tk.Button(window, text="Close", command=window.destroy, bg="white")
        self.close_buttonB.grid(column=0, row=4, columnspan=2)
        self.close_buttonB.config(width=56)

    def open_new_window(self):
        self.new_window = StockGUI(self.master)

    def popup_error_stock_stype(self,window):
        self.popup = tk.Toplevel(window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=310, height=90)
        self.popup.maxsize(width=310, height=90)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=11)
        self.errorLabel = tk.Label(self.popup, text="Symbol and/or path has not been set.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=1, columnspan=4)

    def add_Stock(self):
        if self.symbolText.get() == "":
            self.popup_error_stock_stype(self.stockWindow)
        elif self.startText.get() == "" and self.endText.get() == "":
            try:
                self.current_stock = Stock(symbol=self.symbolText.get(),figsize=(12, 8))
                self.newStockFunctionsGUI = StockFunctionsGUI(self.current_stock, self.stockWindow)
            except:
                self.popup_error_symbol(self.stockWindow)
        elif self.startText.get() != "" and self.endText.get() != "":
            try:
                self.current_stock = Stock(self.symbolText.get(),start=self.startText.get(),end=self.endText.get(),figsize=(12,8))
                self.newStockFunctionsGUI = StockFunctionsGUI(self.current_stock,self.stockWindow)
            except:
                self.popup_error_symbol(self.stockWindow)
        elif self.startText.get() != "" and self.endText.get() == "":
            try:
                self.current_stock = Stock(self.symbolText.get(),start=self.startText.get(),figsize=(12,8))
                self.newStockFunctionsGUI = StockFunctionsGUI(self.current_stock, self.stockWindow)
            except:
                self.popup_error_symbol(self.stockWindow)
        elif self.endText.get() != "" and self.startText.get() == "":
            try:
                self.current_stock = Stock(self.symbolText.get(), end=self.endText.get(),figsize=(12,8))
                self.newStockFunctionsGUI = StockFunctionsGUI(self.current_stock,self.stockWindow)
            except:
                self.popup_error_symbol(self.stockWindow)

    def popup_error_symbol(self,window):
        self.popup = tk.Toplevel(window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=320, height=90)
        self.popup.maxsize(width=320, height=90)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=13)
        self.errorLabel = tk.Label(self.popup, text="Error. Symbol not found.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=1, columnspan=4)

class StockFunctionsGUI():
    def __init__(self,Stock1,master):
        self.master = master
        self.current_stock = Stock1
        self.stock_functions_w = tk.Toplevel(self.master)
        self.stock_functions_w.title(self.current_stock.get_symbol())
        self.stock_functions_w.minsize(width=1200, height=1000)
        self.stock_functions_w.maxsize(width=1200, height=1000)
        self.stock_functions_w.iconbitmap("Images\\fib.ico")
        self.stock_functions_w.configure(background="white")
        self.stock_functions_w.resizable(False, False)
        self.stock_functions_w.rowconfigure(0, weight=1)
        self.stock_functions_w.columnconfigure(0, weight=1)
        self.stock_functions_w.rowconfigure(1, weight=1)
        self.stock_functions_w.columnconfigure(1, weight=1)
        self.stock_functions_w.rowconfigure(2, weight=1)
        self.stock_functions_w.columnconfigure(2, weight=1)
        self.stock_functions_w.rowconfigure(3, weight=1)
        self.stock_functions_w.columnconfigure(3, weight=1)
        self.stock_functions_w.rowconfigure(4, weight=1)
        self.stock_functions_w.columnconfigure(4, weight=1)
        self.stock_functions_w.rowconfigure(5, weight=1)
        self.stock_functions_w.columnconfigure(5, weight=1)
        self.f_save = None
        self.f_close = None
        self.f_vol = None
        self.f_box_close = None
        self.f_log_ret = None
        self.f_mr = None
        self.f_strategy = None
        self.f_mr_and_strat = None
        self.createWidgets(self.stock_functions_w)

    def createWidgets(self,window):
        noButtons = 5
        spaceButtonsx = int(window.winfo_width() / noButtons)
        self.current_stock.set_privates()

        self.menubar = tk.Menu(window)
        self.file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file)
        self.file.add_command(label="Open New Window...", command=self.open_new_window)
        self.file.add_separator()
        self.file.add_command(label="Save as PDF...",command=self.save_as_pdf)
        self.file.add_command(label="Save as PNG...", command=self.save_as_png)
        self.file.add_command(label="Save Full Analysis...", command=self.open_full_analysis_window)
        self.file.add_separator()
        self.file.add_command(label="Close Window", command=window.destroy)


        self.functions = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Functions",menu=self.functions)
        self.functions.add_command(label="Plot Volatility",command=self.plot_volatility)
        self.functions.add_command(label="Plot Close",command=self.plot_close)
        self.functions.add_command(label="Plot Log Return",command=self.plot_log_return)

        self.functions.add_separator()
        self.functions.add_command(label="Plot Market Return",command=self.plot_market_return)
        self.functions.add_command(label="Plot Strategy",command=self.plot_strategy)
        self.functions.add_command(label="Plot Market Return and Strategy",command=self.plot_market_return_and_strategy)

        self.functions.add_separator()
        self.functions.add_command(label="Monte Carlo Simulation",command=self.open_new_montecarlo_window)

        self.functions.add_separator()
        self.functions.add_command(label="Moving Averages",command=self.open_new_ma_window)

        self.functions.add_separator()
        self.functions.add_command(label="Reset Charts",command=self.reset_charts)


        try:
            window.config(menu=self.menubar)
        except AttributeError:
            window.tk.call(self.master, "config", "-menu", self.menubar)

        self.openwindowB = tk.Button(window, text="New " + self.current_stock.get_symbol() + " Window", command=self.open_new_window,
                                       bg="white")
        self.openwindowB.grid(column=0, row=0, )
        self.openwindowB.config(width=spaceButtonsx,height=2)

        self.fullAnalysisB = tk.Button(window, text="Save Full Analysis", command=self.open_full_analysis_window,
                                       bg="white")
        self.fullAnalysisB.grid(column=0, row=1, )
        self.fullAnalysisB.config(width=spaceButtonsx,height=2)

        self.volB = tk.Button(self.stock_functions_w, text="Plot Volatility", command=self.plot_volatility, bg="white")
        self.volB.grid(column=1, row=0)
        self.volB.config(width=spaceButtonsx,height=2)

        self.closeB = tk.Button(self.stock_functions_w, text="Plot Close", command=self.plot_close, bg="white")
        self.closeB.grid(column=1, row=1)
        self.closeB.config(width=spaceButtonsx,height=2)

        self.boxcloseB = tk.Button(self.stock_functions_w, text="Boxplot Close", command=self.plot_box_close, bg="white")
        self.boxcloseB.grid(column=1, row=2)
        self.boxcloseB.config(width=spaceButtonsx,height=2)

        self.logretB = tk.Button(self.stock_functions_w, text="Plot Log Return", command=self.plot_log_return, bg="white")
        self.logretB.grid(column=2, row=0)
        self.logretB.config(width=spaceButtonsx,height=2)

        self.monteCB = tk.Button(self.stock_functions_w, text="Monte Carlo Simulation", command=self.open_new_montecarlo_window,
                                 bg="white")
        self.monteCB.grid(column=2, row=1)
        self.monteCB.config(width=spaceButtonsx,height=2)

        self.mmrsmC = tk.Button(self.stock_functions_w, text="Moving Averages",
                                command=self.open_new_ma_window, bg="white")
        self.mmrsmC.grid(column=2, row=2)
        self.mmrsmC.config(width=spaceButtonsx,height=2)

        self.mrB = tk.Button(self.stock_functions_w, text="Market Return", command=self.plot_market_return, bg="white")
        self.mrB.grid(column=3, row=0)
        self.mrB.config(width=spaceButtonsx,height=2)

        self.strategyB = tk.Button(self.stock_functions_w, text="Strategy", command=self.plot_strategy, bg="white")
        self.strategyB.grid(column=3, row=1)
        self.strategyB.config(width=spaceButtonsx,height=2)

        self.mrasB = tk.Button(self.stock_functions_w, text="Market return and Strategy",
                               command=self.plot_market_return_and_strategy, bg="white")
        self.mrasB.grid(column=3, row=2)
        self.mrasB.config(width=spaceButtonsx,height=2)

        self.updateB = tk.Button(self.stock_functions_w, text="Reset Charts", command=self.reset_charts, bg="white")
        self.updateB.grid(column=0, row=2)
        self.updateB.config(width=spaceButtonsx,height=2)

        self.close_buttonC = tk.Button(self.stock_functions_w, text="Close", command=self.stock_functions_w.destroy,
                                       bg="white")
        self.close_buttonC.grid(column=0, row=3, columnspan=noButtons)
        self.close_buttonC.config(width=self.stock_functions_w.winfo_width(),height=2)

        self.fcanvas = FigureCanvasTkAgg(Figure(figsize=(12, 8)), master=self.stock_functions_w)
        self.fcanvas.get_tk_widget().grid(row=4, columnspan=noButtons)

        self.tbframe = tk.Frame(self.stock_functions_w,bg="white")
        self.tbframe.grid(row=5, columnspan=noButtons)
        self.tbframe.config(width=self.stock_functions_w.winfo_width())

        self.tb = NavigationToolbar2TkAgg(self.fcanvas, self.tbframe)
        self.tb.update()

        self.plot_close()

    def reset_charts(self):
        self.f_save = None
        self.f_close = None
        self.f_vol = None
        self.f_box_close = None
        self.f_log_ret = None
        self.f_mmrs = None
        self.f_mr = None
        self.f_strategy = None
        self.f_mr_and_strat = None
        self.f_box_mmas = None
        self.f_mmas = None
        self.aux = Stock(self.current_stock.get_symbol(),self.current_stock.get_path(),start=self.current_stock.get_start(),figsize=self.current_stock.get_figsize())
        del self.current_stock
        self.current_stock = self.aux
        del self.aux
        self.plot_close()

    def save_as_pdf(self):
        tk.Tk().withdraw()
        path = asksaveasfilename(title="Select a directory to save generated chart.")
        if self.f_save == None:
            self.popup_error_fig(self.stock_functions_w)
        elif path == "":
            pass
        else:
            self.f_save.savefig(path + ".pdf")

    def save_as_png(self):
        tk.Tk().withdraw()
        path = asksaveasfilename(title="Select a directory to save generated chart.")
        if self.f_save == None:
            self.popup_error_fig(self.stock_functions_w)
        elif path == "":
            pass
        else:
            self.f_save.savefig(path + ".png")

    def open_full_analysis_window(self):
        tk.Tk().withdraw()
        path = askdirectory(title="Select a directory to save analysis files.",mustexist=1)
        if path != "":
            self.current_stock.set_path(path)
            self.full_analysis_windows = FullAnalysisGUI(self.current_stock)
        else:
            self.popup_error_path(self.stock_functions_w)


    def open_new_ma_window(self):
        self.ma_window = MMAGUI(self.stock_functions_w,self.current_stock)

    def open_new_montecarlo_window(self):
        self.mc_windows = MonteCarloSimulationsGUI(self.stock_functions_w,self.current_stock)

    def open_new_window(self):
        self.aux_windows = StockFunctionsGUI(self.current_stock,self.stock_functions_w)

    def plot_volatility(self):
        if self.f_vol == None:
            self.f_vol = self.current_stock.plot_volatility()
            self.f_save = self.f_vol
        self.set_plot(self.f_vol)

    def plot_close(self):
        if self.f_close == None:
            self.f_close = self.current_stock.plot_close()
            self.f_save = self.f_close
        self.set_plot(self.f_close)

    def plot_box_close(self):
        if self.f_box_close == None:
            self.f_box_close = self.current_stock.boxplot_close()
            self.f_save = self.f_box_close
        self.set_plot(self.f_box_close)

    def plot_log_return(self):
        if self.f_log_ret == None:
            self.f_log_ret = self.current_stock.plot_log_return()
            self.f_save = self.f_log_ret
        self.set_plot(self.f_log_ret)

    def plot_market_return(self):
        if self.f_mr == None:
            self.f_mr = self.current_stock.plot_market_return()
            self.f_save = self.f_mr
        self.set_plot(self.f_mr)

    def plot_strategy(self):
        if self.f_strategy == None:
            self.f_strategy = self.current_stock.plot_strategy()
            self.f_save = self.f_strategy
        self.set_plot(self.f_strategy)


    def plot_market_return_and_strategy(self):
        if self.f_mr_and_strat == None:
            self.f_mr_and_strat = self.current_stock.plot_market_return_and_strategy()
            self.f_save = self.f_mr_and_strat
        self.set_plot(self.f_mr_and_strat)


    def set_plot(self,f):
        try:
            self.tb.destroy()
            self.fcanvas = FigureCanvasTkAgg(f, master=self.stock_functions_w)
            self.fcanvas.get_tk_widget().grid(row=4, columnspan=4)
            self.tb = NavigationToolbar2TkAgg(self.fcanvas, self.tbframe)
            self.tb.update()
            self.fcanvas.show()
            self.fcanvas.draw()
        except:
            print("Canvas error.")

    def popup_error_path(self,window):
        self.popup = tk.Toplevel(window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=320, height=90)
        self.popup.maxsize(width=320, height=90)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=13)
        self.errorLabel = tk.Label(self.popup, text="Error. You must select a directory.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=1, columnspan=4)

    def popup_error_fig(self,window):
        self.popup = tk.Toplevel(window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=320, height=90)
        self.popup.maxsize(width=320, height=90)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=13)
        self.errorLabel = tk.Label(self.popup, text="Error. You must plot something first.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=1, columnspan=4)

class StockCompareGUI():
    def __init__(self,master):
        self.master = master
        self.stockCWindow = tk.Toplevel(self.master)
        self.stockCWindow.title("Compare Stocks")
        self.stockCWindow.iconbitmap("Images\\fib.ico")
        self.stockCWindow.configure(background="white")
        self.stockCWindow.minsize(width=300, height=110)
        self.stockCWindow.maxsize(width=300, height=110)
        self.stockCWindow.resizable(False, False)
        self.createWidgets(self.stockCWindow)
        self.stockCWindow.rowconfigure(0,weight=1)
        self.stockCWindow.rowconfigure(1, weight=1)
        self.stockCWindow.rowconfigure(2, weight=1)
        self.stockCWindow.rowconfigure(3, weight=1)
        self.stockCWindow.rowconfigure(4, weight=1)
        self.stockCWindow.rowconfigure(5, weight=1)
        self.stockCWindow.rowconfigure(6, weight=1)
        self.stockCWindow.rowconfigure(7, weight=1)
        self.stockCWindow.columnconfigure(0, weight=1)
        self.stockCWindow.columnconfigure(1, weight=1)
        self.stockCWindow.columnconfigure(2, weight=1)
        self.stockCWindow.columnconfigure(3, weight=1)

    def createWidgets(self,window):

        self.menubar = tk.Menu(window)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.menu)
        self.menu.add_command(label="Open New Window", command=self.open_new_window)
        self.menu.add_separator()
        self.menu.add_command(label="Close Window", command=window.destroy)
        try:
            window.config(menu=self.menubar)
        except AttributeError:
            window.tk.call(self.master, "config", "-menu", self.menubar)

        self.symbol1Text = tk.Entry(window)
        self.symbol1Text.grid(column=1, row=0)
        self.symbol1Label = tk.Label(window, text="Enter first stock symbol: ", bg="white")
        self.symbol1Label.grid(column=0, row=0)

        self.symbol2Text = tk.Entry(window)
        self.symbol2Text.grid(column=1, row=1)
        self.symbol2Label = tk.Label(window, text="Enter second stock symbol: ", bg="white")
        self.symbol2Label.grid(column=0, row=1)


        self.addStockC = tk.Button(window, text="Compare Stocks", command=self.add_comparison_stocks, bg="white")
        self.addStockC.grid(column=0, row=2, columnspan=2)
        self.addStockC.config(width=70)

        self.close_buttonC = tk.Button(window, text="Close", command=self.stockCWindow.destroy, bg="white")
        self.close_buttonC.grid(column=0, row=3, columnspan=2)
        self.close_buttonC.config(width=70)

    def open_new_window(self):
        self.newWindow = StockCompareGUI(self.stockCWindow)


    def add_comparison_stocks(self):
        if self.symbol1Text.get() == "" or self.symbol2Text.get() == "":
            self.popup_error_stock_comparison(self.stockCWindow)
        else:
            notError = True
            try:
                self.current_stock = Stock(self.symbol1Text.get(), figsize=(12, 8))
            except:
                self.popup_error_symbol1(self.stockCWindow)
                notError = False
            try:
                self.stock_to_compare = Stock(self.symbol2Text.get(),figsize=(12,8))
                if notError == True:
                    self.newStockCompareFunctionsGUI = StockCompareFunctionsGUI(self.stockCWindow, self.current_stock,
                                                                            self.stock_to_compare)
            except:
                self.popup_error_symbol2(self.stockCWindow)

    def popup_error_stock_comparison(self,window):
        self.popup = tk.Toplevel(window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=320, height=90)
        self.popup.maxsize(width=320, height=90)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=10)
        self.errorLabel = tk.Label(self.popup, text="Error. Symbols and/or path has not been set.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=1, columnspan=4)

    def popup_error_symbol1(self,window):
        self.popup = tk.Toplevel(window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=320, height=90)
        self.popup.maxsize(width=320, height=90)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=13)
        self.errorLabel = tk.Label(self.popup, text="Error. Symbol #1 not found.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=1, columnspan=4)

    def popup_error_symbol2(self,window):
        self.popup = tk.Toplevel(window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=320, height=90)
        self.popup.maxsize(width=320, height=90)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=13)
        self.errorLabel = tk.Label(self.popup, text="Error. Symbol #2 not found.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=1, columnspan=4)



class StockCompareFunctionsGUI():
    def __init__(self,master,Stock1,Stock2):
        self.master = master
        self.current_stock = Stock1
        self.stock_to_compare = Stock2
        self.compare_stock_w = tk.Toplevel(self.master)
        self.compare_stock_w.title(self.current_stock.get_symbol() + " and " + self.stock_to_compare.get_symbol() + " Comparison")
        self.compare_stock_w.minsize(width=1200, height=920)
        self.compare_stock_w.maxsize(width=1200, height=920)
        self.compare_stock_w.iconbitmap("Images\\fib.ico")
        self.compare_stock_w.configure(background="white")
        self.compare_stock_w.resizable(False, False)
        self.compare_stock_w.rowconfigure(0, weight=1)
        self.compare_stock_w.columnconfigure(0, weight=1)
        self.compare_stock_w.rowconfigure(1, weight=1)
        self.compare_stock_w.columnconfigure(1, weight=1)
        self.compare_stock_w.rowconfigure(2, weight=1)
        self.compare_stock_w.columnconfigure(2, weight=1)
        self.compare_stock_w.rowconfigure(3, weight=1)
        self.compare_stock_w.columnconfigure(3, weight=1)
        self.compare_stock_w.rowconfigure(4, weight=1)
        self.compare_stock_w.columnconfigure(4, weight=1)
        self.compare_stock_w.rowconfigure(5, weight=1)
        self.compare_stock_w.columnconfigure(5, weight=1)
        self.createWidgets(self.compare_stock_w)
        self.f_save = None
        self.f_rets = None
        self.f_reg = None
        self.f_corr = None
        self.f_close = None

    def createWidgets(self,window):
        noButtons = 6
        noButtonc = 3
        spaceButtonsx = int(window.winfo_width() / noButtons)
        spaceButtonsy = int(window.winfo_width() / noButtonc)
        self.current_stock.set_privates()
        self.stock_to_compare.set_privates()


        self.menubar = tk.Menu(window)
        self.file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file)
        self.file.add_command(label="Open New Window...", command=self.open_new_window)
        self.file.add_separator()
        self.file.add_command(label="Save as PDF...",command=self.save_as_pdf)
        self.file.add_command(label="Save as PNG...", command=self.save_as_png)
        self.file.add_command(label="Save Full Comparison...", command=self.full_comparison)
        self.file.add_separator()
        self.file.add_command(label="Close Window", command=window.destroy)


        self.functions = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Functions",menu=self.functions)
        self.functions.add_command(label="Plot Correlation",command=self.plot_rolling_corr_between)
        self.functions.add_command(label="Plot Regression",command=self.plot_regression_between)
        self.functions.add_separator()
        self.functions.add_command(label="Compare Log Returns",command=self.plot_rets_between)
        self.functions.add_command(label="Compare Close Prices",command=self.plot_close_between)

        self.functions.add_separator()
        self.functions.add_command(label="Reset Charts",command=self.reset_charts)

        try:
            window.config(menu=self.menubar)
        except AttributeError:
            window.tk.call(self.master, "config", "-menu", self.menubar)

        self.openwindowB = tk.Button(window,text="Open new "+ self.current_stock.get_symbol() + " and " + self.stock_to_compare.get_symbol() +" Comparison Window",command=self.open_new_window, bg="white")
        self.openwindowB.grid(column=0,row=0)
        self.openwindowB.config(width=window.winfo_width()/3)


        self.full_comparison_B = tk.Button(window, text="Save Full Comparison",
                                           command=self.full_comparison, bg="white")
        self.full_comparison_B.grid(column=0, row=1)
        self.full_comparison_B.config(width=window.winfo_width() / 3)

        self.returnsbetween_B = tk.Button(window, text="Compare Log Returns",
                                          command=self.plot_rets_between, bg="white")
        self.returnsbetween_B.grid(column=1, row=0)
        self.returnsbetween_B.config(width=window.winfo_width() / 3)

        self.regression_between_B = tk.Button(window, text="Plot Regression", command=self.plot_regression_between,
                                              bg="white")
        self.regression_between_B.grid(column=1, row=1)
        self.regression_between_B.config(width=window.winfo_width() / 3)
        try:
            self.rolling_cor_between_B = tk.Button(window, text="Plot Correlation",
                                                   command=self.plot_rolling_corr_between, bg="white")
            self.rolling_cor_between_B.grid(column=2, row=0)
            self.rolling_cor_between_B.config(width=window.winfo_width() / 4)
        except:
            print("Dates are not valid for correlation, skipping...")
        self.close_between_B = tk.Button(window, text="Plot and Compare Close Prices", command=self.plot_close_between,
                                         bg="white")
        self.close_between_B.grid(column=2, row=1)
        self.close_between_B.config(width=window.winfo_width() / 3)

        self.resetB = tk.Button(window, text="Reset Charts", command=self.reset_charts,
                                       bg="white")
        self.resetB.grid(column=3, row=0)
        self.resetB.config(width=window.winfo_width() / 4)


        self.close_buttonD = tk.Button(window, text="Close window", command=self.compare_stock_w.destroy,
                                       bg="white")
        self.close_buttonD.grid(column=3, row=1)
        self.close_buttonD.config(width=window.winfo_width() / 3)

        self.fcanvas = FigureCanvasTkAgg(Figure(figsize=(12, 8)), master=window)
        self.fcanvas.get_tk_widget().grid(row=4, columnspan=noButtons)

        self.tbframe = tk.Frame(window)
        self.tbframe.grid(row=5, columnspan=noButtons)
        self.tbframe.config(width=window.winfo_width())

        self.tb = NavigationToolbar2TkAgg(self.fcanvas, self.tbframe)
        self.tb.update()

    def open_new_window(self):
        self.newwindow = StockCompareFunctionsGUI(self.compare_stock_w,self.current_stock,self.stock_to_compare)

    def save_as_pdf(self):
        tk.Tk().withdraw()
        path = asksaveasfilename(title="Select a directory to save generated chart.")
        if self.f_save == None:
            self.popup_error_fig(self.compare_stock_w)
        elif path == "":
            pass
        else:
            self.f_save.savefig(path + ".pdf")

    def save_as_png(self):
        tk.Tk().withdraw()
        path = asksaveasfilename(title="Select a directory to save generated chart.")
        if self.f_save == None:
            self.popup_error_fig(self.compare_stock_w)
        elif path == "":
            pass
        else:
            self.f_save.savefig(path + ".png")

    def reset_charts(self):
        self.f_rets = None
        self.f_reg = None
        self.f_corr = None
        self.f_close = None
        self.f_save = None
        self.aux = Stock(self.current_stock.get_symbol(), self.current_stock.get_path(),
                         start=self.current_stock.get_start(), figsize=self.current_stock.get_figsize())
        del self.current_stock
        self.current_stock = self.aux
        del self.aux
        self.aux = Stock(self.stock_to_compare.get_symbol(), self.stock_to_compare.get_path(),
                         start=self.current_stock.get_start(), figsize=self.current_stock.get_figsize())
        self.set_plot(Figure(figsize=(12,8)))

    def full_comparison(self):
        tk.Tk().withdraw()
        path = askdirectory(title="Select a directory to save comparison files.", mustexist=1)
        if path != "":
            self.current_stock.set_path(path)
            try:
                self.current_stock.compare_with(self.stock_to_compare)
            except:
                pass
        else:
            pass


    def plot_rets_between(self):
        if self.f_rets == None:
            self.f_rets = self.current_stock.plot_rets_between(self.stock_to_compare)
            self.f_save = self.f_rets
        self.set_plot(self.f_rets)


    def plot_regression_between(self):
        if self.f_reg == None:
            self.f_reg = self.current_stock.plot_regression_between(self.stock_to_compare)
            self.f_save = self.f_reg
        self.set_plot(self.f_reg)

    def plot_rolling_corr_between(self):
        try:
            if self.f_corr == None:
                self.f_corr = self.current_stock.plot_rolling_corr_between(self.stock_to_compare)
                self.f_save = self.f_corr
            self.set_plot(self.f_corr)
        except:
            print("Dates are not valid for correlation, skipping...")


    def plot_close_between(self):
        if self.f_close == None:
            self.f_close = self.current_stock.plot_close_between(self.stock_to_compare)
            self.f_save = self.f_close
        self.set_plot(self.f_close)

    def set_plot(self,f):
        self.tb.destroy()
        self.fcanvas = FigureCanvasTkAgg(f, master=self.compare_stock_w)
        self.fcanvas.get_tk_widget().grid(row=4, columnspan=6)
        self.tb = NavigationToolbar2TkAgg(self.fcanvas, self.tbframe)
        self.tb.update()
        self.fcanvas.show()
        self.fcanvas.draw()

    def popup_error_fig(self,window):
        self.popup = tk.Toplevel(window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=320, height=90)
        self.popup.maxsize(width=320, height=90)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=13)
        self.errorLabel = tk.Label(self.popup, text="Error. You must plot something first.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=1, columnspan=4)
"""
CLASS CURRENTLY UNDER DEVELOPMENT
class Sp500GUI():
    def __init__(self,master=None):
        self.master = master
        self.sp500Window = tk.Toplevel(self.master)
        self.sp500Window.title("S&P500")
        self.sp500Window.iconbitmap("Images\\fib.ico")
        self.sp500Window.configure(background="white")
        self.sp500Window.minsize(width=400, height=118)
        self.sp500Window.maxsize(width=400, height=118)
        self.sp500Window.resizable(False, False)
        self.createWidgets()

    def createWidgets(self):
        self.startText = tk.Entry(self.sp500Window)
        self.startText.grid(column=1, row=0)
        self.startLabel = tk.Label(self.sp500Window, text="Enter start date(format: 'YEAR-DAY-MONTH'): ", bg="white")
        self.startLabel.grid(column=0, row=0)

        self.endText = tk.Entry(self.sp500Window)
        self.endText.grid(column=1, row=1)
        self.endLabel = tk.Label(self.sp500Window, text="Enter end date(format: 'YEAR-DAY-MONTH'): ", bg="white")
        self.endLabel.grid(column=0, row=1)

        self.pathText = tk.Entry(self.sp500Window)
        self.pathText.grid(column=1, row=2)
        self.pathLabel = tk.Label(self.sp500Window, text="Enter a path to save generated files : ", bg="white")
        self.pathLabel.grid(column=0, row=2)

        self.startAnalysis_B = tk.Button(self.sp500Window, text="Start Analysis of All S&P500",
                                         command=self.analyzeSP500,
                                         bg="white")
        self.startAnalysis_B.grid(column=0, row=3,columnspan=2)
        self.startAnalysis_B.config(width=56)

        self.close_buttonB = tk.Button(self.sp500Window, text="Close", command=self.sp500Window.destroy, bg="white")
        self.close_buttonB.grid(column=0, row=4, columnspan=2)
        self.close_buttonB.config(width=56)



    def analyzeSP500(self):
        if self.pathText.get() == "":
            self.popup_error_stock_stype()
        elif self.startText.get() == "" and self.endText.get() == "":
           # os.system("SP500.py " + self.pathText.get())
            path = self.pathText.get()
            def callback():
               subprocess.call([sys.executable, "./SP500.py", path])
            a = threading.Thread(target=callback)
            a.start()
        elif self.startText.get() != "" and self.endText.get() != "":
            def callback():
                subprocess.call([sys.executable, "./SP500.py", self.startText.get(), self.endText.get()])
            a = threading.Thread(target=callback)
            a.start()
            #os.system("SP500.py " + self.pathText.get() +" "+self.startText.get() +" "+ self.endText.get())
        elif self.startText.get() != "" and self.endText.get() == "":
            def callback():
                subprocess.call([sys.executable,"./SP500.py",self.pathText.get(),self.startText.get()])
            a = threading.Thread(target=callback)
            a.start()
            #os.system("SP500.py " + self.pathText.get() + " " +  self.startText.get())
        elif self.endText.get() != "" and self.startText.get() == "":
            def callback():
                subprocess.call([sys.executable,"./SP500.py",self.pathText.get(),"2000-01-01",self.endText.get()])
            a = threading.Thread(target=callback)
            a.start()
            #os.system("SP500.py " + self.pathText.get() + " " + self.endText.get())


    def popup_error_stock_stype(self):
        self.popup = tk.Toplevel(self.sp500Window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=310, height=90)
        self.popup.maxsize(width=310, height=90)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=10)
        self.errorLabel = tk.Label(self.popup, text="Error. Path has not been set.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=1, columnspan=4)
"""

class MonteCarloSimulationsGUI():
    def __init__(self,master,Stock1):
        self.master = master
        self.MCWindow = tk.Toplevel(self.master)
        self.current_stock = Stock1
        self.MCWindow.title(Stock1.get_symbol() + " Monte Carlo Simulation")
        self.MCWindow.iconbitmap("Images\\fib.ico")
        self.MCWindow.configure(background="white")
        self.MCWindow.minsize(width=400, height=117)
        self.MCWindow.maxsize(width=400, height=117)
        self.MCWindow.resizable(False, False)
        self.createWidgets(self.MCWindow)

    def createWidgets(self,window):

        self.menubar = tk.Menu(window)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.menu)
        self.menu.add_command(label="Open New Window", command=self.open_new_window)
        self.menu.add_separator()
        self.menu.add_command(label="Close Window", command=window.destroy)
        try:
            window.config(menu=self.menubar)
        except AttributeError:
            window.tk.call(self.master, "config", "-menu", self.menubar)

        self.setI = tk.Entry(self.MCWindow)
        self.setI.grid(column=1, row=0)
        self.ILabel = tk.Label(self.MCWindow, text="Enter the number of simulations (Default: 10000): ", bg="white")
        self.ILabel.grid(column=0, row=0)

        self.periodText = tk.Entry(self.MCWindow)
        self.periodText.grid(column=1, row=1)
        self.periodLabel = tk.Label(self.MCWindow, text="Enter period (Default: 252): ", bg="white")
        self.periodLabel.grid(column=0, row=1)

        self.runSimulationB = tk.Button(self.MCWindow, text="Run Simulations", command=self.open_simulation_window, bg="white")
        self.runSimulationB.grid(column=0, row=4, columnspan=2)
        self.runSimulationB.config(width=56)

        self.close_buttonB = tk.Button(self.MCWindow, text="Close", command=self.MCWindow.destroy, bg="white")
        self.close_buttonB.grid(column=0, row=5, columnspan=2)
        self.close_buttonB.config(width=56)

    def open_new_window(self):
        self.new_window = MonteCarloSimulationsGUI(self.MCWindow,self.current_stock)


    def open_simulation_window(self):
        if self.setI.get() == "" and self.periodText.get() == "":
            self.I = 10000
            self.T = 252
        elif self.setI.get() != "" and self.periodText.get() == "":
            self.T =252
            if not str(self.setI.get()).isdigit():
                self.popup_error_invalid_input(self.MCWindow)
            else:
                self.I = int(self.setI.get())
        elif self.setI.get() != "" and self.periodText.get() != "":
            if not str(self.setI.get()).isdigit() or not str(self.periodText.get()).isdigit():
                self.popup_error_invalid_input(self.MCWindow)
            else:
                self.T = int(self.periodText.get())
                self.I = int(self.setI.get())
        elif self.setI.get() == "" and self.periodText.get() != "":
            if not str(self.periodText.get()).isdigit():
                self.popup_error_invalid_input(self.MCWindow)
            else:
                self.T = int(self.periodText.get())
                self.I = int(10000)
        self.MCFunctionsWindow = MonteCarloSimulationFunctionsGUI(self.MCWindow,self.current_stock,self.I,self.T)

    def popup_error_invalid_input(self,window):
        self.popup = tk.Toplevel(window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=330, height=90)
        self.popup.maxsize(width=330, height=90)
        self.popup.rowconfigure(0,weight=1)
        self.popup.rowconfigure(1,weight=1)
        self.popup.rowconfigure(2,weight=1)
        self.popup.columnconfigure(0,weight=1)
        self.popup.columnconfigure(2, weight=1)
        self.popup.columnconfigure(3, weight=1)
        self.popup.columnconfigure(4, weight=1)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0, rowspan=2)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=20)
        self.errorLabel = tk.Label(self.popup, text="Error. Invalid input.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=2, columnspan=4)

class MonteCarloSimulationFunctionsGUI():
    def __init__(self,master,Stock1,I,T):
        self.master = master
        self.current_stock = Stock1
        self.I = I
        self.T = T
        self.current_stock = Stock1
        self.mc_functions_w = tk.Toplevel(self.master)
        self.mc_functions_w.title(self.current_stock.get_symbol() +" " +str(self.I) + " Monte Carlo Simulations")
        self.mc_functions_w.minsize(width=1200, height=920)
        self.mc_functions_w.maxsize(width=1200, height=920)
        self.mc_functions_w.iconbitmap("Images\\fib.ico")
        self.mc_functions_w.configure(background="white")
        self.mc_functions_w.resizable(False, False)
        self.mc_functions_w.rowconfigure(0, weight=1)
        self.mc_functions_w.columnconfigure(0, weight=1)
        self.mc_functions_w.rowconfigure(1, weight=1)
        self.mc_functions_w.columnconfigure(1, weight=1)
        self.mc_functions_w.rowconfigure(2, weight=1)
        self.mc_functions_w.columnconfigure(2, weight=1)
        self.mc_functions_w.rowconfigure(3,weight=1)
        self.mc_functions_w.columnconfigure(3,weight=1)
        self.mc_functions_w.columnconfigure(4,weight=1)
        self.mc_functions_w.columnconfigure(5,weight=1)
        self.createWidgets(self.mc_functions_w)
        self.f_smc = None
        self.f_save = None
        self.f_mmc = None
        self.f_hmmc = None

    def createWidgets(self,window):
        noButtons = 5
        spaceButtonsx = int(self.mc_functions_w.winfo_width() / noButtons)

        self.menubar = tk.Menu(window)
        self.file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file)
        self.file.add_command(label="Open New Window...", command=self.open_new_window)
        self.file.add_separator()
        self.file.add_command(label="Save as PDF...", command=self.save_as_pdf)
        self.file.add_command(label="Save as PNG...", command=self.save_as_png)
        self.file.add_separator()
        self.file.add_command(label="Close Window", command=window.destroy)

        self.functions = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Functions", menu=self.functions)
        self.functions.add_command(label="Plot Single Monte Carlo Simulation", command=self.plot_mc)
        self.functions.add_command(label="Plot All Simulations", command=self.plot_multiple_mc)
        self.functions.add_command(label="Plot Histogram of All Simulations", command=self.plot_hist_multiple_mc)

        self.functions.add_separator()
        self.functions.add_command(label="Reset Charts", command=self.reset_charts)

        try:
            window.config(menu=self.menubar)
        except AttributeError:
            window.tk.call(self.master, "config", "-menu", self.menubar)

        self.openwindowB = tk.Button(self.mc_functions_w, text="New " + self.current_stock.get_symbol() + " Window",
                                     command=self.open_new_window,
                                     bg="white")
        self.openwindowB.grid(column=0, row=0, )
        self.openwindowB.config(width=spaceButtonsx,height=6)

        self.singleMCB = tk.Button(self.mc_functions_w, text="Plot Histogram of Single Simulation", command=self.plot_mc,
                                       bg="white")
        self.singleMCB.grid(column=1, row=0)
        self.singleMCB.config(width=spaceButtonsx,height=6)

        self.multipleMCB = tk.Button(self.mc_functions_w, text="Plot All Simulations", command=self.plot_multiple_mc, bg="white")
        self.multipleMCB.grid(column=2, row=0)
        self.multipleMCB.config(width=spaceButtonsx,height=6)

        self.histmultipleB = tk.Button(self.mc_functions_w, text="Plot Histogram of All Simulations", command=self.plot_hist_multiple_mc, bg="white")
        self.histmultipleB.grid(column=3, row=0)
        self.histmultipleB.config(width=spaceButtonsx,height=6)

        self.resetB = tk.Button(self.mc_functions_w, text="Reset Charts", command=self.reset_charts,
                                bg="white")
        self.resetB.grid(column=4, row=0)
        self.resetB.config(width=spaceButtonsx,height=6)

        self.closeB = tk.Button(self.mc_functions_w, text="Close Window", command=self.mc_functions_w.destroy,
                                   bg="white")
        self.closeB.grid(column=5, row=0)
        self.closeB.config(width=spaceButtonsx,height=6)

        self.fcanvas = FigureCanvasTkAgg(Figure(figsize=(12, 8)), master=self.mc_functions_w)
        self.fcanvas.get_tk_widget().grid(row=2, columnspan=noButtons)

        self.tbframe = tk.Frame(self.mc_functions_w)
        self.tbframe.grid(row=3, columnspan=noButtons)
        self.tbframe.config(width=self.mc_functions_w.winfo_width())

        self.tb = NavigationToolbar2TkAgg(self.fcanvas, self.tbframe)
        self.tb.update()

    def save_as_pdf(self):
        tk.Tk().withdraw()
        path = asksaveasfilename(title="Select a directory to save generated chart.")
        if self.f_save == None:
            self.popup_error_fig(self.mc_functions_w)
        elif path == "":
            pass
        else:
            self.f_save.savefig(path + ".pdf")

    def save_as_png(self):
        tk.Tk().withdraw()
        path = asksaveasfilename(title="Select a directory to save generated chart.")
        if self.f_save == None:
            self.popup_error_fig(self.mc_functions_w)
        elif path == "":
            pass
        else:
            self.f_save.savefig(path + ".png")

    def reset_charts(self):
        self.f_smc = None
        self.f_save = None
        self.f_mmc = None
        self.f_hmmc = None
        self.aux = Stock(self.current_stock.get_symbol(), self.current_stock.get_path(),
                         start=self.current_stock.get_start(), figsize=self.current_stock.get_figsize())
        del self.current_stock
        self.current_stock = self.aux
        del self.aux
        self.set_plot(Figure(figsize=(12, 8)))

    def open_new_window(self):
        self.aux_windows = MonteCarloSimulationFunctionsGUI(self.mc_functions_w,self.current_stock,self.I,self.T)


    def plot_mc(self):
        if self.f_smc == None:
            self.f_smc = self.current_stock.plot_monte_carlo_simulation(self.I)
            self.f_save = self.f_smc
        self.set_plot(self.f_smc)


    def plot_multiple_mc(self):
        if self.f_mmc == None:
            self.f_mmc = self.current_stock.plot_n_mcs_chart_to_pdf(self.I , self.T)
            self.f_save = self.f_mmc
        self.set_plot(self.f_mmc)

    def plot_hist_multiple_mc(self):
        if self.f_hmmc == None:
            self.f_hmmc = self.current_stock.plot_n_mcs_hist_daily_returns(self.I, self.T)
            self.f_save = self.f_hmmc
        self.set_plot(self.f_hmmc)

    def set_plot(self,f):
        self.tb.destroy()
        self.fcanvas = FigureCanvasTkAgg(f, master=self.mc_functions_w)
        self.fcanvas.get_tk_widget().grid(row=2, columnspan=6)

        self.tb = NavigationToolbar2TkAgg(self.fcanvas, self.tbframe)
        self.tb.update()
        self.fcanvas.show()
        self.fcanvas.draw()

    def popup_error_fig(self, window):
        self.popup = tk.Toplevel(window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=320, height=90)
        self.popup.maxsize(width=320, height=90)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=13)
        self.errorLabel = tk.Label(self.popup, text="Error. You must plot something first.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=1, columnspan=4)



class MMAGUI():
    def __init__(self,master,Stock1):
        self.master = master
        self.MAsWindow = tk.Toplevel(self.master)
        self.current_stock = Stock1
        self.MAsWindow.title(Stock1.get_symbol() + " Moving Averages")
        self.MAsWindow.iconbitmap("Images\\fib.ico")
        self.MAsWindow.configure(background="white")
        self.MAsWindow.minsize(width=400, height=100)
        self.MAsWindow.maxsize(width=400, height=100)
        self.MAsWindow.resizable(False, False)
        self.MAsWindow.rowconfigure(0, weight=1)
        self.MAsWindow.rowconfigure(1, weight=1)
        self.MAsWindow.rowconfigure(2, weight=1)
        self.MAsWindow.rowconfigure(3, weight=1)
        self.MAsWindow.columnconfigure(0, weight=1)
        self.MAsWindow.columnconfigure(1, weight=1)
        self.createWidgets(self.MAsWindow)

    def createWidgets(self,window):

        self.menubar = tk.Menu(window)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.menu)
        self.menu.add_command(label="Open New Window", command=self.open_new_window)
        self.menu.add_separator()
        self.menu.add_command(label="Close Window", command=window.destroy)
        try:
            window.config(menu=self.menubar)
        except AttributeError:
            window.tk.call(self.master, "config", "-menu", self.menubar)

        self.setMA1 = tk.Entry(window)
        self.setMA1.grid(column=1, row=0)
        self.MA1Label = tk.Label(window, text="Enter Moving Average #1(Default: 42): ", bg="white")
        self.MA1Label.grid(column=0, row=0)

        self.setMA2 = tk.Entry(window)
        self.setMA2.grid(column=1, row=1)
        self.MA2Label = tk.Label(window, text="Enter Moving Average #2 (Default: 252): ", bg="white")
        self.MA2Label.grid(column=0, row=1)

        self.runMAB = tk.Button(window, text="Continue", command=self.open_mma_functions_window,
                                        bg="white")
        self.runMAB.grid(column=0, row=2, columnspan=2)
        self.runMAB.config(width=56)

        self.close_buttonB = tk.Button(window, text="Close", command=window.destroy, bg="white")
        self.close_buttonB.grid(column=0, row=3, columnspan=2)
        self.close_buttonB.config(width=56)

    def open_mma_functions_window(self):
        if self.setMA1.get() == "" and self.setMA2.get() == "":
            self.MA1 = 42
            self.MA2 = 252
        elif self.setMA1.get() != "" and self.setMA2.get() == "":
            self.MA2 = 252
            self.MA1= int(self.setMA1.get())
        elif self.setMA1.get() != "" and self.setMA2.get() != "":
            self.MA1 = int(self.setMA1.get())
            self.MA2 = int(self.setMA2.get())
        elif self.setMA1.get() == "" and self.setMA2.get() != "":
            self.MA2 = int(self.setMA2.get())
            self.MA1 = 42
        try:
            self.current_stock.set_privates(self.MA1,self.MA2)
            self.MAFunctionsWindow = MMAFunctionsGUI(self.MAsWindow,self.current_stock,self.MA1,self.MA2)
        except:
            self.popup_error_MA(self.MAsWindow)

    def open_new_window(self):
        self.new_window = MMAGUI(self.MAsWindow,self.current_stock)

    def popup_error_MA(self, window):
        self.popup = tk.Toplevel(window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=310, height=90)
        self.popup.maxsize(width=310, height=90)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=10)
        self.errorLabel = tk.Label(self.popup, text="Error. Invalid Moving Averages.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=1, columnspan=4)

class MMAFunctionsGUI():
    def __init__(self,master,Stock1,MA1,MA2):
        self.master = master
        self.MAFunctionsWindow = tk.Toplevel(self.master)
        self.MA1 = MA1
        self.MA2 = MA2
        self.current_stock = Stock1
        self.MAFunctionsWindow.title(Stock1.get_symbol() + " " + str(self.MA1) + "-" + str(self.MA2) + " Moving Averages")
        self.MAFunctionsWindow.iconbitmap("Images\\fib.ico")
        self.MAFunctionsWindow.configure(background="white")
        self.MAFunctionsWindow.minsize(width=1200, height=920)
        self.MAFunctionsWindow.maxsize(width=1200, height=920)
        self.MAFunctionsWindow.resizable(False, False)
        self.MAFunctionsWindow.rowconfigure(0, weight=1)
        self.MAFunctionsWindow.rowconfigure(1, weight=1)
        self.MAFunctionsWindow.rowconfigure(2, weight=1)
        self.MAFunctionsWindow.columnconfigure(0, weight=1)
        self.MAFunctionsWindow.columnconfigure(1, weight=1)
        self.MAFunctionsWindow.columnconfigure(2, weight=1)
        self.MAFunctionsWindow.columnconfigure(3, weight=1)
        self.MAFunctionsWindow.columnconfigure(4, weight=1)
        self.MAFunctionsWindow.columnconfigure(5, weight=1)
        self.f_save = None
        self.f_mmrs = None
        self.f_box_mmas = None
        self.f_mmas = None
        self.createWidgets(self.MAFunctionsWindow)

    def createWidgets(self,window):
        noButtons = 6
        noButtonc = 3
        spaceButtonsx = int(window.winfo_width() / noButtons)
        spaceButtonsy = int(window.winfo_width() / noButtonc)

        self.menubar = tk.Menu(window)
        self.file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file)
        self.file.add_command(label="Open New Window...", command=self.open_new_mma_window)
        self.file.add_separator()
        self.file.add_command(label="Save as PDF...", command=self.save_as_pdf)
        self.file.add_command(label="Save as PNG...", command=self.save_as_png)
        self.file.add_separator()
        self.file.add_command(label="Close Window", command=window.destroy)

        self.functions = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Functions", menu=self.functions)
        self.functions.add_command(label="Boxplot "+ str(self.MA1) + "-"+ str(self.MA2) + " MAs", command=self.plot_box_multiple_mas)
        self.functions.add_command(label="Plot " + str(self.MA1) + "-" + str(self.MA2) + " MAs",
                                   command=self.plot_mul_mas)
        self.functions.add_command(label="Plot " + str(self.MA1) + "-"+ str(self.MA2) + " with Regime", command=self.plot_multiple_ma_regime_strategy_mr)

        self.functions.add_separator()
        self.functions.add_command(label="Reset Charts", command=self.reset_charts)

        try:
            window.config(menu=self.menubar)
        except AttributeError:
            window.tk.call(self.master, "config", "-menu", self.menubar)

        self.newwindowB = tk.Button(window, text="New " +self.current_stock.get_symbol()+ " Window" ,command=self.open_new_mma_window,bg="white")
        self.newwindowB.grid(column=0, row=0)
        self.newwindowB.config(width=spaceButtonsx)

        self.bpmaB = tk.Button(window, text="Boxplot "+ str(self.MA1) + "-"+ str(self.MA2) + " MAs", command=self.plot_box_multiple_mas,
                               bg="white")
        self.bpmaB.grid(column=1, row=0)
        self.bpmaB.config(width=spaceButtonsx)

        self.mmaB = tk.Button(window, text="Plot "+ str(self.MA1) + "-"+ str(self.MA2) + " MAs", command=self.plot_mul_mas, bg="white")
        self.mmaB.grid(column=2, row=0)
        self.mmaB.config(width=spaceButtonsx)

        self.mmrsB = tk.Button(window, text="Plot " + str(self.MA1) + "-"+ str(self.MA2) + " with Regime", command=self.plot_multiple_ma_regime_strategy_mr, bg="white")
        self.mmrsB.grid(column=3, row=0)
        self.mmrsB.config(width=spaceButtonsx)

        self.resetB = tk.Button(window, text="Reset Charts",
                               command=self.reset_charts,
                               bg="white")
        self.resetB.grid(column=4, row=0)
        self.resetB.config(width=spaceButtonsx)

        self.closeB = tk.Button(window, text="Close",command=window.destroy, bg="white")
        self.closeB.grid(column=5, row=0)
        self.closeB.config(width=spaceButtonsx)


        self.fcanvas = FigureCanvasTkAgg(Figure(figsize=(12, 8)), master=window)
        self.fcanvas.get_tk_widget().grid(row=1, columnspan=noButtons)

        self.tbframe = tk.Frame(window)
        self.tbframe.grid(row=2, columnspan=noButtons)
        self.tbframe.config(width=window.winfo_width())

        self.tb = NavigationToolbar2TkAgg(self.fcanvas, self.tbframe)
        self.tb.update()

    def reset_charts(self):
        self.f_mmrs = None
        self.f_box_mmas = None
        self.f_mmas =None
        self.f_save = None
        self.aux = Stock(self.current_stock.get_symbol(), self.current_stock.get_path(),
                         start=self.current_stock.get_start(), figsize=self.current_stock.get_figsize())
        del self.current_stock
        self.current_stock = self.aux
        del self.aux
        self.set_plot(Figure(figsize=(12, 8)))

    def save_as_pdf(self):
        path = asksaveasfilename(title="Select a directory to save generated chart.")
        if self.f_save == None:
            self.popup_error_fig(self.MAFunctionsWindow)
        elif path == "":
            pass
        else:
            self.f_save.savefig(path + ".pdf")

    def save_as_png(self):
        path = asksaveasfilename(title="Select a directory to save generated chart.")
        if self.f_save == None:
            self.popup_error_fig(self.MAFunctionsWindow)
        elif path == "":
            pass
        else:
            self.f_save.savefig(path + ".png")

    def open_new_mma_window(self):
        self.newWindow = MMAFunctionsGUI(self.MAFunctionsWindow,self.current_stock,self.MA1,self.MA2)

    def plot_multiple_ma_regime_strategy_mr(self):
        if self.f_mmrs == None:
            self.f_mmrs = self.current_stock.plot_multiple_ma_regime_strategy_mr(self.MA1,self.MA2)
            self.f_save = self.f_mmrs
        self.set_plot(self.f_mmrs)

    def plot_box_multiple_mas(self):
        if self.f_box_mmas == None:
            self.f_box_mmas = self.current_stock.boxplot_multiple_mas(self.MA1,self.MA2)
            self.f_save = self.f_box_mmas
        self.set_plot(self.f_box_mmas)


    def plot_mul_mas(self):
        if self.f_mmas == None:
            self.f_mmas = self.current_stock.plot_multiple_mas(self.MA1,self.MA2)
            self.f_save = self.f_box_mmas
        self.set_plot(self.f_mmas)

    def set_plot(self,f):
        self.tb.destroy()
        self.fcanvas = FigureCanvasTkAgg(f, master=self.MAFunctionsWindow)
        self.fcanvas.get_tk_widget().grid(row=1, columnspan=6)

        self.tb = NavigationToolbar2TkAgg(self.fcanvas, self.tbframe)
        self.tb.update()
        self.fcanvas.show()
        self.fcanvas.draw()

    def popup_error_fig(self,window):
        self.popup = tk.Toplevel(window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=320, height=90)
        self.popup.maxsize(width=320, height=90)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=13)
        self.errorLabel = tk.Label(self.popup, text="Error. You must plot something first.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=1, columnspan=4)

class FullAnalysisGUI():
    def __init__(self,Stock1):
        self.AnalysisWindow = tk.Toplevel()
        self.current_stock = Stock1
        self.AnalysisWindow .title(Stock1.get_symbol() + " Full Analysis")
        self.AnalysisWindow .iconbitmap("Images\\fib.ico")
        self.AnalysisWindow .configure(background="white")
        self.AnalysisWindow .minsize(width=480, height=150)
        self.AnalysisWindow .maxsize(width=480, height=150)
        self.AnalysisWindow .resizable(False, False)
        self.AnalysisWindow.rowconfigure(0, weight=1)
        self.AnalysisWindow.rowconfigure(1, weight=1)
        self.AnalysisWindow.rowconfigure(2, weight=1)
        self.AnalysisWindow.rowconfigure(3, weight=1)
        self.AnalysisWindow.rowconfigure(4, weight=1)
        self.AnalysisWindow.rowconfigure(5, weight=1)
        self.AnalysisWindow.columnconfigure(0, weight=1)
        self.AnalysisWindow.columnconfigure(1, weight=1)
        self.createWidgets()

    def createWidgets(self):
        self.setI = tk.Entry(self.AnalysisWindow)
        self.setI.grid(column=1, row=0)
        self.ILabel = tk.Label(self.AnalysisWindow, text="Enter the number of Monte Carlo Simulations (Default: 10000): ", bg="white")
        self.ILabel.grid(column=0, row=0)

        self.periodText = tk.Entry(self.AnalysisWindow)
        self.periodText.grid(column=1, row=1)
        self.periodLabel = tk.Label(self.AnalysisWindow, text="Enter period for Monte Carlo Simulations(Default: 252): ", bg="white")
        self.periodLabel.grid(column=0, row=1)

        self.MA1Text = tk.Entry(self.AnalysisWindow)
        self.MA1Text.grid(column=1, row=2)
        self.MA1Label = tk.Label(self.AnalysisWindow , text="Enter Moving Average #1 (Default: 42): ",
                                    bg="white")
        self.MA1Label.grid(column=0, row=2)

        self.MA2Text = tk.Entry(self.AnalysisWindow)
        self.MA2Text.grid(column=1, row=3)
        self.MA2Label = tk.Label(self.AnalysisWindow, text="Enter Moving Average #2 (Default: 252) ",
                                    bg="white")
        self.MA2Label.grid(column=0, row=3)

        self.runAnalysisB = tk.Button(self.AnalysisWindow, text="Run Full Analysis", command=self.open_simulation_window, bg="white")
        self.runAnalysisB.grid(column=0, row=4, columnspan=2)
        self.runAnalysisB.config(width=self.AnalysisWindow.winfo_width())

        self.close_buttonB = tk.Button(self.AnalysisWindow, text="Close", command=self.AnalysisWindow.destroy, bg="white")
        self.close_buttonB.grid(column=0, row=5, columnspan=2)
        self.close_buttonB.config(width=self.AnalysisWindow.winfo_width())


    def open_simulation_window(self):
        self.I = None
        self.T =None
        self.MA1 = None
        self.MA2 = None
        if self.setI.get() == "" and self.periodText.get() == "":
            self.I = 10000
            self.T = 252
        elif self.setI.get() != "" and self.periodText.get() == "":
            self.T =252
            if not str(self.setI.get()).isdigit():
                self.popup_error_invalid_input(self.AnalysisWindow)
            else:
                self.I = int(self.setI.get())
        elif self.setI.get() != "" and self.periodText.get() != "":
            if not str(self.setI.get()).isdigit() or not str(self.periodText.get()).isdigit():
                self.popup_error_invalid_input(self.AnalysisWindow)
            else:
                self.T = int(self.periodText.get())
                self.I = int(self.setI.get())
        elif self.setI.get() == "" and self.periodText.get() != "":
            if not str(self.periodText.get()).isdigit():
                self.popup_error_invalid_input(self.AnalysisWindow)
            else:
                self.T = int(self.periodText.get())
                self.I = int(10000)

        if self.MA1Text.get() == "" and self.MA2Text.get() == "":
            self.MA1 = 42
            self.MA2 = 252
        elif self.MA1Text.get() != "" and self.MA2Text.get() != "":
            if not str(self.MA1Text.get()).isdigit() or not str(self.MA2Text.get()).isdigit():
                self.popup_error_invalid_input(self.AnalysisWindow)
            else:
                self.MA1 = int(self.MA1Text.get())
                self.MA2 = int(self.MA2Text.get())
        elif self.MA2Text.get() != "" and self.MA1Text.get() == "":
            if not str(self.MA2Text.get()).isdigit():
                self.popup_error_invalid_input(self.AnalysisWindow)
            else:
                self.MA1 = 42
                self.MA2 = int(self.MA2Text.get())
        elif self.MA1Text.get() != "" and self.MA2Text.get() == "":
            if not str(self.MA1Text.get()).isdigit():
                self.popup_error_invalid_input(self.AnalysisWindow)
            else:
                self.MA1 = int(self.MA1Text.get())
                self.MA2 = 252
        if self.I != None and self.MA1 != None and self.MA2 != None and self.T != None:
            self.current_stock.full_analysis(self.I,self.T,self.MA1,self.MA2)

    def popup_error_invalid_input(self,window):
        self.popup = tk.Toplevel(window)
        self.popup.title("Error")
        self.popup.iconbitmap("Images\\fib.ico")
        self.popup.configure(background="white")
        self.popup.minsize(width=330, height=90)
        self.popup.maxsize(width=330, height=90)
        self.popup.rowconfigure(0,weight=1)
        self.popup.rowconfigure(1,weight=1)
        self.popup.rowconfigure(2,weight=1)
        self.popup.columnconfigure(0,weight=1)
        self.popup.columnconfigure(2, weight=1)
        self.popup.columnconfigure(3, weight=1)
        self.popup.columnconfigure(4, weight=1)
        self.popup.resizable(False, False)

        self.errorImg = Image.open("Images\\error.png")
        self.errorImg = self.errorImg.resize((50, 50), Image.ANTIALIAS)
        self.errorImg = ImageTk.PhotoImage(self.errorImg)
        self.errorImgpan = tk.Label(self.popup, image=self.errorImg, borderwidth=0, background="white")
        self.errorImgpan.grid(column=0, row=0, rowspan=2)
        self.errorImgpan.grid_propagate(0)

        self.errorFont = tkFont.Font(family="Abadi MT Condensed Light", size=20)
        self.errorLabel = tk.Label(self.popup, text="Error. Invalid input.",
                                   font=self.errorFont, bg="white")
        self.errorLabel.grid(column=1, row=0, columnspan=3)

        self.close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, bg="white")
        self.close_button.grid(column=0, row=2, columnspan=4)

