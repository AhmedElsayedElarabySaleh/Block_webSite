#!/usr/bin/python3

# import Important modules
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from os import path
import sys
import time
from datetime import datetime as dt
# import UI file
FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),'Blocker_WebSite.ui'))

class mainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(mainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Ui()
        self.handel_Button()
        self.Block = Run_App() # To Take Object From QThread 
        self.Block.finished.connect(self.finished_stop) #Connect Signal From QThread To Func In Main Thread
        self.Block.start_a.connect(self.start_Oper) # Connect Signal _________


    def Handel_Ui(self):
        # To Center Window In Screen
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setWindowTitle("Blocker App")
        self.setFixedSize(635,290)


    def handel_Button(self):
        self.pushButton.clicked.connect(self.onstart)
        self.pushButton_3.clicked.connect(self.Add_WebSite)
        self.pushButton_4.clicked.connect(self.Clear_Item)
        self.pushButton_2.clicked.connect(self.stop_app)
        self.pushButton_5.clicked.connect(self.Restore_Host_File)

    def Add_WebSite(self):# Add Website From LineEdit To ListWidget
        self.listWidget.addItem(self.lineEdit.text())
        self.lineEdit.setText('')
        self.lineEdit.setFocus()

    def Start(self):#Start Time
        s = QTime.toPyTime (self.timeEdit.time())#Convert Qtime to Datetime.time
        return s
         
        # print (type(QTime.toPyTime (self.timeEdit.time())))

    def End(self):
        x = QTime.toPyTime (self.timeEdit_2.time())#Convert Qtime to Datetime.time
        return x 

             


    def Item (self): # To Iterate all item in ListWedgit
        website_list = [self.listWidget.item(i).text() for i in range(self.listWidget.count())]
        return website_list


    def Clear_Item(self):#To Clear ListWidget
        self.listWidget.clear()


    def onstart(self):# To Start Thread And App
        self.Block.start_1 = QTime.toPyTime (self.timeEdit.time())
        self.Block.end = QTime.toPyTime (self.timeEdit_2.time())
        self.Block.list_item = [self.listWidget.item(i).text() for i in range(self.listWidget.count())]
        self.Block.running = True
        self.Block.start()

    def stop_app(self): #To Stop Functions
        self.Block.Stop_Run()

    def finished_stop(self): # To Take Signal From Thread And Make QMessageBox
        QMessageBox.information(self,'Stop','The App Is Stopped !') # To Show MessageBox

    def start_Oper(self):# Take Signal From Thread And Make QMessageBox
        QMessageBox.information(self,'Start','The App Is Start ^_^') # To Show MessageBox

    def Restore_Host_File(self):
        host_path = r"C:\Window\System32\drivers\etc\hosts" 
        with open (host_path , 'r+' ) as file :
            new_f = file.readlines()
            file.seek(0)
            for line in new_f:
                if "www" not in line and '127.0.0.1' not in line :
                    file.write(line)
            file.truncate()
            file.seek(0)
        QMessageBox.information(self,'$ Restore Default $','Restored ^_^ ')


class Run_App(QThread):
    start_a = pyqtSignal()
    stop = pyqtSignal()
    running = True
    def run (self):
        host_path = r"C:\Window\System32\drivers\etc\hosts" 
        redirect = '127.0.0.1'
        self.start_a.emit()
        while self.running :
            if self.start_1 < dt.now().time() < self.end :# To Check Time Start < Now < End 
                with open (host_path , 'r+') as file : # Open The Host File 
                    content = file.read()
                    for website in self.list_item: # Loop On All WebSite In ListWidget
                        if website in content:
                            pass
                        else :
                            file.write(redirect + ' ' + website+'\n') # Write redirect + website To Block It 
            else:
                with open(host_path , 'r+') as file:# Else That 
                    content = file.readlines()#read every Line in file
                    file.seek(0)#Make Seek In The First 
                    for line in content:#Make Iterate On All Line 
                        if not any(website in line for website in self.list_item): # if Not Var(WebSite) Not In   line and Make loop on Var(WebSite) in ListWidegt
                            file.write(line)#Write line 
                    file.truncate()  # To delete All word are iterate
            time.sleep(5) #Sleep 10 secound 
         
    def Stop_Run(self):
        self.running = False
        self.stop.emit()



def main():
    app = QApplication(sys.argv)
    window = mainApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()