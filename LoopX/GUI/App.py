from FRONTEND import *

class MenuApp(Lib.threading.Thread):

    def __init__(self):
        Lib.threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = Lib.tk.Tk()
        menu = MenuGUI.MenuGUI(self.root)
        self.root.mainloop()



if __name__ == '__main__':
    app  = MenuApp()



