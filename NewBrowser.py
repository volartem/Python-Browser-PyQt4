# -*- coding: cp1251 -*-
import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtWebKit


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1000, 500)
        self.windowView()

    def windowView(self):
        self.progr = QtGui.QProgressBar()
        self.statusBar().addPermanentWidget(self.progr)
        self.progr.setTextVisible(False)
        self.progr.setVisible(False)
        self.widgett = Tabb(self, "https://www.youtube.com/")  #Central TABWidget on Windows YouTube dont work
        self.widgett.setTabsClosable(True)
        self.widgett.setMovable(True)
        self.setCentralWidget(self.widgett)                    ####### Install Central Widget in MainWindow
        self.setWindowIcon(QtGui.QIcon("WebBro.png"))

class Tabb(QtGui.QTabWidget):
    def __init__(self, this, url, parent=None):
        super(Tabb, self).__init__(parent)
        self.this = this
        self.webTabList = []
        self.addTab(" ", url)
        self.tabCloseRequested.connect(self.closeTab)
        #self.addPlusButton()                          # use later

    def addPlusButton(self):
        self.tabButton = QtGui.QToolButton(self)
        self.tabButton.setText('  +  ')
        font = self.tabButton.font()
        font.setBold(True)
        self.tabButton.setFont(font)
        self.setCornerWidget(self.tabButton)
        self.tabButton.clicked.connect(self.addTab)
        self.tabCloseRequested.connect(self.closeTab)

    def addTab(self, ddd, urll="about:blank"):   #  reimplement addTab()
        ddd = " "
        input_tab = QtGui.QWidget()             ## input widget
        super().addTab(input_tab, ddd)

        contV = QtGui.QVBoxLayout(input_tab)
        contH = QtGui.QHBoxLayout()
        contV.addLayout(contH)

        button = QtGui.QPushButton("->")
        button2 = QtGui.QPushButton("<-")
        button3 = QtGui.QPushButton("ReLoad")
        button4 = QtGui.QPushButton("+")
        button3.setStatusTip('Reload')
        button2.setStatusTip('Back')
        button.setStatusTip('Go')
        contH.addWidget(button3)
        contH.addWidget(button2)
        contH.addWidget(button)
        textLine = QtGui.QLineEdit()
        contH.addWidget(textLine)
        contH.addWidget(button4)

        web = self.createWeb(urll)
        contV.addWidget(web)

        self.engineTab(button, button2, button3, button4, textLine, web)

        indexx = self.indexOf(web.parent())
        self.setCurrentIndex(indexx)
        self.setTabShape(QtGui.QTabWidget.Rounded)

    def createWeb(self, urll):
        web = WebView(urll)
        return web

    def closeTab(self, ind):
        obj = self.widget(ind)
        self.removeTab(ind)
        obj.deleteLater()

    def engineTab(self, but, but2, but3, but4, texT, web=None):

        def statusChanged(link):
            self.this.statusBar().showMessage(link)
        def urlChanged():
            text = texT.text()
            web.setUrl(QtCore.QUrl(text))
        def reload():
            web.setUrl(QtCore.QUrl(texT.text()))

        def back():
            page = web.page()
            history = page.history()
            history.back()

        def next():
            page = web.page()
            history = page.history()
            history.forward()

        def titleChangedd(title):
            icon = web.icon()
            self.setIconSize(QtCore.QSize(16, 16))
            i = self.indexOf(web.parent())
            self.this.setWindowTitle(title)
            self.setTabText(i, title)
            self.setTabIcon(i, QtGui.QIcon(icon))
        def linkChanged(link):
            texT.setText(link.toString())
        def loadProgress(set):
            self.this.progr.setValue(set)
            self.this.progr.setVisible(True)
        def loadProgressEnd(set):
            if set == True:
                self.this.progr.setVisible(False)

        def indexChanged(ind):
            tex = self.tabText(ind)
            self.this.setWindowTitle(tex)

        web.titleChanged.connect(lambda title: titleChangedd(title))                         ### 1 type
        QtCore.QObject.connect(web, QtCore.SIGNAL("linkClicked (const QUrl&)"), linkChanged) ### 2 type
        QtCore.QObject.connect(web, QtCore.SIGNAL("urlChanged (const QUrl&)"), linkChanged)
        QtCore.QObject.connect(web, QtCore.SIGNAL("loadProgress(int)"), loadProgress)
        QtCore.QObject.connect(web, QtCore.SIGNAL("loadFinished(bool)"), loadProgressEnd)
        but4.clicked.connect(self.addTab)                                                    ### 3 type
        web.page().linkHovered.connect(statusChanged)
        QtCore.QObject.connect(but2, QtCore.SIGNAL("clicked()"), back)
        QtCore.QObject.connect(but3, QtCore.SIGNAL("clicked()"), reload)
        QtCore.QObject.connect(but, QtCore.SIGNAL("clicked()"), next)
        QtCore.QObject.connect(texT, QtCore.SIGNAL("returnPressed()"), urlChanged)
        self.currentChanged.connect(lambda ind: indexChanged(ind))

class WebView(QtWebKit.QWebView):
    def __init__(self, url, parent=None):
        super(WebView, self).__init__(parent)
        self.load(QtCore.QUrl(url))
        self.newTabAction = QtGui.QAction('Open in New Tab', self)
        self.newTabAction.triggered.connect(self.createNewTab)

    def createNewTab(self):
        this = self.parent().parent().parent()
        url = self.newTabAction.data()
        this.addTab("+", url)


    def contextMenuEvent(self, event):
        menu = self.page().createStandardContextMenu()
        hit = self.page().currentFrame().hitTestContent(event.pos())
        url = hit.linkUrl()
        if url.isValid():
            self.newTabAction.setData(url)
            menu.addAction(self.newTabAction)
        menu.exec_(event.globalPos())


if __name__ == "__main__":
     app = QtGui.QApplication(sys.argv)
     windows = MainWindow()
     windows.show()
     sys.exit(app.exec_())