from Lib import *
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 00:28:40 2017

@author: Jorge Alberto Niño Cabal
version: 0.1

THIS MODULE IS CURRENTLY UNDER DEVELOPMENT
"""


class SP500AppJarGUI():
    def __init__(self,path,start="2000-01-01",end=dt.datetime.now()):

        self.path = path
        self.gui = appJar.gui()
        self.gui.setResizable(canResize=False)
        self.gui.setBg("white")
        self.gui.setTitle("S&P500 Analysis Progress")
        self.gui.setGeometry(500,70)
        self.start = start
        self.end = end
        self.createWidgets()
        self.progressp = 0
        self.gui.registerEvent(self.updateMeter)
        self.gui.setIcon("Images\\"
                         "fib.ico")
        self.argv = sys.argv[1:]
        with open(self.path + "\Progress\Progress.txt","w") as aux:
            aux.write(str(self.progressp))
        self.gui.go()


    def createWidgets(self):
        self.gui.addSplitMeter("progress")
        self.gui.setMeterFill("progress",["green","red"])
        def callback(btn):
            self.sp500analysis()
        self.gui.addButton("Begin",callback,colspan=3)

    def sp500analysis(self):
        def callback():
            subprocess.call([sys.executable, "./Finalprocess.py"] + self.argv)
        a = threading.Thread(target=callback)
        a.start()


    def updateMeter(self):
        Stock.check_if_progress_exists(self.path)
        with open(self.path + "\Progress\Progress.txt", "r") as aux:
            self.progressp = int(aux.readlines()[0])
            self.gui.setMeter("progress",self.progressp)

if len(sys.argv) == 4:
    app = SP500AppJarGUI(path=str(sys.argv[1]),start=str(sys.argv[2]),end=str(sys.argv[3]))
elif len(sys.argv) == 3:
    app = SP500AppJarGUI(path=str(sys.argv[1]), start=str(sys.argv[2]))
elif len(sys.argv) == 2:
    app = SP500AppJarGUI(path=str(sys.argv[1]))
else:
    app = SP500AppJarGUI(path=str("C:\\Users\\jorge\\Midas"))
