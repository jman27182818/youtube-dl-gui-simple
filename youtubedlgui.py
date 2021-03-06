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
from PyQt4.QtCore import QRunnable
from PyQt4.QtCore import QThreadPool

class system_thread(QRunnable):
    def __init__(self,command):
        QThread.__init__(self)
        self.command = command

    @pyqtSlot()
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

        self.isdown=False
        self.threadpool = QThreadPool()

        self.statusbutton = QPushButton("Status")
        self.statusbutton.clicked.connect(self.checkstatus)
        grid.addWidget(self.statusbutton,3,1)

        self.urlcache = []

        self.setLayout(grid)
        self.setWindowTitle("Youtube Downloader")

    def checkstatus(self):
        status = "Currently Downloading "
        status += str(self.threadpool.activeThreadCount() )
        status += " videos"
        self.edit.append(status)
        
    def startdownload(self):
        
        self.isdown = True
        qtext = self.browser.url()
        texttot=str(qtext)
        #bad bodge to get url
        textarray = texttot.split("'")
        text = textarray[1]
        if text not in self.urlcache:
            self.urlcache.append(text)
            print(self.urlcache)
        else:
            return
        if(self.audiocheckbox.isChecked()):
            strr="cd ~/Music/ && youtube-dl -i --extract-audio --audio-format mp3 "
        else:
            strr = "cd ~/Videos/ && youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' --password PASSWORD -i -url "

        strr +="'"
        strr += text
        strr += "'"

        worker = system_thread(strr)
        #self.connect(self.runthread,SIGNAL("finished()"),self.done)
        self.threadpool.start(worker)

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
