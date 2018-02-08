import sys
import os
import subprocess
import signal

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QTextEdit
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import QProcess
from PyQt4.QtCore import QString
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import QThread
from PyQt4.QtWebKit import QWebView
from PyQt4.QtGui import QGridLayout, QLineEdit, QWidget


class system_thread(QThread):
    def __init__(self,command):
        QThread.__init__(self)
        self.command = command
        self.proc = None


    def __del__(self):
        self.wait()

    def run(self):
        os.system(str(self.command))

class MyWindow(QWidget):
    def __init__(self, parent = None):
        super(MyWindow,self).__init__(parent)
        #create grid layout
        grid = QGridLayout()
        # text edit
        self.edit = QTextEdit(self)
        self.edit.setReadOnly(True)
        # browser
        self.browser = QWebView()
        self.browser.load(QUrl("http://www.youtube.com"))
        #cehck box
        self.audiocheckbox = QCheckBox("Audio Only") 
        #creat button
        self.downbutton = QPushButton("Download")
        self.downbutton.clicked.connect(self.startdownload)
        # add browser at top
        grid.addWidget(self.browser, 1, 0,1,2) # spans two colums
        grid.addWidget(self.audiocheckbox,2,1)

        #add buttion 2,0
        grid.addWidget(self.downbutton,2,0)
        grid.addWidget(self.edit,3,0)

        self.runthread = None
        self.isdown=False

        self.setLayout(grid)
        self.setWindowTitle("Youtube Downloader")

    def startdownload(self):
        if(self.isdown):
            self.edit.append("Currently downloading a video: Press Ctrl-C in terminal to stop prior download")
            return
        
        self.isdown = True
        qtext = self.browser.url()
        texttot=str(qtext)
        #bad bodge to get url
        textarray = texttot.split("'")
        text = textarray[1]
        if(self.audiocheckbox.isChecked()):
            strr="cd ~/Music/ && youtube-dl --extract-audio --audio-format mp3 "
        else:
            strr = "cd ~/Videos/ && youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' --password PASSWORD -i -url "

        strr +="'"
        strr += text
        strr += "'"

        self.runthread = system_thread(strr)
        self.connect(self.runthread,SIGNAL("finished()"),self.done)
        self.runthread.start()

        self.edit.append("Download has started")
        self.edit.append("[Check status in terminal]")
        self.edit.append("[To kill download press Ctrl-C in the associated terminal] \n")


    def done(self):
        self.edit.append("DOWNLOAD COMPLETE \n")
        self.isdown = False



def main():
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
