# -*- coding: utf-8 -*-
import sys
import re
import urllib.request
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtWebKit


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1000, 500)
        self.menu_bar = self.menuBar()
        self.menuEngine()
        self.windowView()

    def menuEngine(self):
        podmenu1 = self.menu_bar.addMenu("File")

        self.history = self.menu_bar.addMenu("History")
        self.allHistory = QtGui.QAction("All History", self)
        self.history.addAction(self.allHistory)

        self.historyView()

        podmenu3 = self.menu_bar.addMenu("Help")

        exit = QtGui.QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        about = QtGui.QAction("About", self)
        about.setIconVisibleInMenu(True)
        about.setIcon(QtGui.QIcon("images/WebBro.png"))

        podmenu1.addAction(exit)
        podmenu3.addAction(about)
        about.triggered.connect(self.aboutView)

    def historyView(self):
        self.modHistorWindow = QtGui.QWidget(self, QtCore.Qt.Window)
        self.modHistorWindow.setWindowIcon(QtGui.QIcon("images/WebBro.png"))
        self.modHistorWindow.setWindowTitle("History")
        self.modHistorWindow.resize(500, 300)
        self.hbox = QtGui.QHBoxLayout(self.modHistorWindow)

    def windowView(self):
        self.progr = QtGui.QProgressBar()
        self.statusBar().addPermanentWidget(self.progr)
        self.progr.setTextVisible(False)
        self.progr.setVisible(False)
        self.widgett = Tabb(self, "https://google.com")
        self.widgett.setTabsClosable(True)
        self.widgett.setMovable(True)
        self.setCentralWidget(self.widgett)
        self.setWindowIcon(QtGui.QIcon("images/WebBro.png"))

    def aboutView(self):
        mod_window = QtGui.QWidget(self, QtCore.Qt.Window)
        mod_window.setWindowIcon(QtGui.QIcon("images/WebBro.png"))
        mod_window.setWindowTitle("About NewBrowser")
        mod_window.setFixedSize(500, 332)
        horLayout = QtGui.QHBoxLayout(mod_window)
        localHtmls = QtWebKit.QWebView()
        localHtmls.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)

        localHtmls.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        localHtmls.load(QtCore.QUrl("about.html"))
        horLayout.addWidget(localHtmls)
        localHtmls.linkClicked.connect(self.clicks)
        mod_window.show()

    def clicks(self, url):
        self.widgett.addTabb(url)

class Tabb(QtGui.QTabWidget):
    def __init__(self, this, url, parent=None):
        super(Tabb, self).__init__(parent)
        self.this = this
        self.setIconSize(QtCore.QSize(16, 16))
        self.webHistoryListt = []
        self.addTabb(url)
        # self.addPlusButton()
        self.tabCloseRequested.connect(self.closeTab)

    def addPlusButton(self):
        self.tabButton = QtGui.QToolButton(self)
        self.tabButton.setText('  +  ')
        font = self.tabButton.font()
        font.setBold(True)
        self.tabButton.setFont(font)
        self.setCornerWidget(self.tabButton)
        self.tabButton.clicked.connect(lambda: self.addTabb())

    def addTabb(self,  urll="start.html"):
        input_tab = QtGui.QWidget()
        super().addTab(input_tab, " ")

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

        # web = WebView()
        web = self.createWeb(urll)
        contV.addWidget(web)

        self.engineTab(button, button2, button3, button4, textLine, web)

        indexx = self.indexOf(web.parent())
        self.setCurrentIndex(indexx)
        self.setTabShape(QtGui.QTabWidget.Rounded)

        self.setStyleSheet('QTabBar::tab { width: 100px; height: 25px; }')
        self.setElideMode(QtCore.Qt.ElideRight)

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
            i = self.indexOf(web.parent())
            self.this.setWindowTitle(title)
            self.setTabText(i, title)

        def linkChanged(link):
            try:
                texT.setText(link.toString())
                i = self.indexOf(web.parent())
                link = link.toString()
                result = re.split(r'/', link)
                url = "https://www.google.com/s2/favicons?domain=" + result[2]
                data = urllib.request.urlopen(url).read()
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(data)
                icon = QtGui.QIcon(pixmap)
                self.setTabIcon(i, icon)
            except:
                self.setTabIcon(i, QtGui.QIcon("images/WebBro.png"))

            self.createWebList(link)

        def loadProgress(set):
            self.this.progr.setValue(set)
            self.this.progr.setVisible(True)

        def loadProgressEnd(set):
            if set == True:
                self.this.progr.setVisible(False)

        def indexChanged(ind):
            tex = self.tabText(ind)
            self.this.setWindowTitle(tex)

        def historyEngineViev():
            for j in range(self.this.hbox.count()):
                self.this.hbox.itemAt(j).widget().deleteLater()

            tablHistor = QtGui.QTableWidget(len(self.webHistoryListt), 1)
            header = tablHistor.horizontalHeader()
            header.setStretchLastSection(True)

            tablHistor.setHorizontalHeaderLabels("   Url   ;")
            self.this.hbox.addWidget(tablHistor)
            tablHistor.verticalHeader().hide()

            i = 0
            for j in self.webHistoryListt:
                tablHistor.setItem(i, 0, QtGui.QTableWidgetItem(j))
                i += 1
            tablHistor.itemDoubleClicked.connect(lambda item: self.addTabb(item.text()))
            self.this.modHistorWindow.show()

        web.titleChanged.connect(lambda title: titleChangedd(title))
        QtCore.QObject.connect(web, QtCore.SIGNAL("urlChanged (const QUrl&)"), linkChanged)
        QtCore.QObject.connect(web, QtCore.SIGNAL("loadProgress(int)"), loadProgress)
        QtCore.QObject.connect(web, QtCore.SIGNAL("loadFinished(bool)"), loadProgressEnd)
        but4.clicked.connect(lambda : self.addTabb())
        web.page().linkHovered.connect(statusChanged)
        QtCore.QObject.connect(but2, QtCore.SIGNAL("clicked()"), back)
        QtCore.QObject.connect(but3, QtCore.SIGNAL("clicked()"), reload)
        QtCore.QObject.connect(but, QtCore.SIGNAL("clicked()"), next)
        QtCore.QObject.connect(texT, QtCore.SIGNAL("returnPressed()"), urlChanged)
        self.currentChanged.connect(lambda ind: indexChanged(ind))
        self.this.history.triggered.connect(lambda: historyEngineViev())

    def createWebList(self, item):
        nesovpad = True
        if len(self.webHistoryListt) == 0:
            self.webHistoryListt.append(item)
            nesovpad = False
        else:
            for i in self.webHistoryListt:
                if i == item:
                    nesovpad = False
                    break
        if nesovpad:
            self.webHistoryListt.append(item)

class WebView(QtWebKit.QWebView):
    def __init__(self, url, parent=None):
        super(WebView, self).__init__(parent)
        self.load(QtCore.QUrl(url))
        self.newTabAction = QtGui.QAction('Open Link in New Tab', self)
        self.newTabAction.triggered.connect(self.createNewTab)
        self.settings().globalSettings().setAttribute(QtWebKit.QWebSettings.LocalStorageEnabled, True)
        self.settings().setLocalStoragePath("/home/Python Browser/Storage/")

    def createNewTab(self):
        this = self.parent().parent().parent()
        url = self.newTabAction.data()
        this.addTabb(url)

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