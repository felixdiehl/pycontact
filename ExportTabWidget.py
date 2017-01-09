from PyQt5.QtWidgets import QTabWidget, QWidget, QGridLayout, QLabel, QPushButton, QComboBox, QLineEdit
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from Plotters import *
from ErrorBox import ErrorBox
class ExportTabWidget(QTabWidget):

    valueUpdated = pyqtSignal(str, str)

    def __init__(self, parent = None):
       super(ExportTabWidget, self).__init__(parent)

       self.tab1 = QWidget()
       self.tab2 = QWidget()
       self.tab3 = QWidget()

       self.addTab(self.tab1, "View")
       self.addTab(self.tab2, "Histogram")
       self.addTab(self.tab3, "Contact Map")
       self.tab1UI()
       self.tab2UI()
       self.tab3UI()
       self.setWindowTitle("Export")
       self.contacts = []
       self.threshold = 0
       self.nsPerFrame = 0
       self.map1 = None
       self.map2 = None

    def setThresholdAndNsPerFrame(self, currentThreshold, currentNsPerFrame):
        self.threshold = currentThreshold
        self.nsPerFrame = currentNsPerFrame

    def tab1UI(self):
        grid = QGridLayout()
        self.tab1.setLayout(grid)

        self.tab1.exportLabel = QLabel("Export current view: ")

        self.tab1.saveButton = QPushButton("Export")
        self.tab1.saveButton.setAutoDefault(False)
        self.tab1.saveButton.clicked.connect(self.pushSave)

        self.tab1.formatBox = QComboBox()
        self.tab1.formatBox.addItem("PNG")
        self.tab1.formatBox.addItem("SVG")

        grid.addWidget(self.tab1.exportLabel, 0, 0)
        grid.addWidget(self.tab1.saveButton, 0, 1)

        grid.addWidget(self.tab1.formatBox, 2, 0)


    def tab2UI(self):
        self.grid1 = QGridLayout()
        self.tab2.setLayout(self.grid1)

        self.tab2.histPlot = HistPlotter(None, width=8, height=5, dpi=60)
        self.grid1.addWidget(self.tab2.histPlot, 3, 0, 1, 4)

        self.tab2.histTypeBox = QComboBox()
        self.tab2.histTypeBox.addItem("General Histogram")
        self.tab2.histTypeBox.addItem("Bin per Contact")

        self.grid1.addWidget(self.tab2.histTypeBox, 0, 3)

        self.tab2.attributeBox = QComboBox()
        self.tab2.attributeBox.addItem("Mean Score")
        self.tab2.attributeBox.addItem("Median Score")
        self.tab2.attributeBox.addItem("Mean Lifetime")
        self.tab2.attributeBox.addItem("Median Lifetime")
        self.tab2.attributeBox.addItem("Hbond percentage")

        self.grid1.addWidget(self.tab2.attributeBox, 1, 3)

        self.tab2.plotButton = QPushButton("Show Preview")
        self.tab2.plotButton.setAutoDefault(False)
        self.tab2.plotButton.clicked.connect(self.pushPlot)
        self.grid1.addWidget(self.tab2.plotButton, 0, 0, 1, 3)

        self.tab2.saveButton = QPushButton("Save Histogram")
        self.tab2.saveButton.setAutoDefault(False)
        self.tab2.saveButton.clicked.connect(self.saveHist)
        self.grid1.addWidget(self.tab2.saveButton, 1, 0, 1, 1)

        self.tab2.formatLabel = QLabel("Format: ")
        self.grid1.addWidget(self.tab2.formatLabel, 1, 1)

        self.tab2.xTicksFontSizeLabel = QLabel("bin per contact font size: ")
        self.grid1.addWidget(self.tab2.xTicksFontSizeLabel, 2, 0)

        self.tab2.xTicksFontSizeField = QLineEdit("11")
        self.grid1.addWidget(self.tab2.xTicksFontSizeField, 2, 1)

        self.tab2.formatBox = QComboBox()
        self.tab2.formatBox.addItem("pdf")
        self.tab2.formatBox.addItem("png")
        self.tab2.formatBox.addItem("svg")
        self.tab2.formatBox.addItem("eps")
        self.grid1.addWidget(self.tab2.formatBox, 1, 2)

    def tab3UI(self):
        self.grid2 = QGridLayout()
        self.tab3.setLayout(self.grid2)

        self.tab3.mapPlot = MapPlotter(None, width=8, height=5, dpi=60)
        self.grid2.addWidget(self.tab3.mapPlot, 3, 0, 1, 4)

        self.tab3.plotMapButton = QPushButton("Show Preview")
        self.tab3.plotMapButton.setAutoDefault(False)
        self.tab3.plotMapButton.clicked.connect(self.pushMapPlot)
        self.grid2.addWidget(self.tab3.plotMapButton, 0, 0, 1, 1)

        self.tab3.formatBox = QComboBox()
        self.tab3.formatBox.addItem("pdf")
        self.tab3.formatBox.addItem("png")
        self.tab3.formatBox.addItem("svg")
        self.tab3.formatBox.addItem("eps")
        self.grid2.addWidget(self.tab3.formatBox, 0, 2, 1, 1)

        self.tab3.saveButton = QPushButton("Save Map")
        self.tab3.saveButton.setAutoDefault(False)
        self.tab3.saveButton.clicked.connect(self.saveMap)
        self.grid2.addWidget(self.tab3.saveButton, 0, 3, 1, 1)

        self.tab3.attributeBox = QComboBox()
        self.tab3.attributeBox.addItem("Mean Score")
        self.tab3.attributeBox.addItem("Median Score")
        self.tab3.attributeBox.addItem("Mean Lifetime")
        self.tab3.attributeBox.addItem("Median Lifetime")
        self.tab3.attributeBox.addItem("Hbond percentage")

        self.grid2.addWidget(self.tab3.attributeBox, 0, 1)

    def saveHist(self):
        self.plotHist()

        fileName = QFileDialog.getSaveFileName(self, 'Export Path')
        if len(fileName[0]) > 0:
            path, file_extension = os.path.splitext(fileName[0])
            self.tab2.histPlot.saveFigure(path, self.tab2.formatBox.currentText())

    def saveMap(self):
        self.plotMap()

        fileName = QFileDialog.getSaveFileName(self, 'Export Path')
        if len(fileName[0]) > 0:
            path, file_extension = os.path.splitext(fileName[0])
            self.tab3.mapPlot.saveFigure(path, self.tab3.formatBox.currentText())

    def pushPlot(self):
        self.plotHist()

    def pushMapPlot(self):
        self.plotMap()

    def plotHist(self):
        sip.delete(self.tab2.histPlot)
        self.tab2.histPlot = HistPlotter(None, width=8, height=5, dpi=60)
        self.grid1.addWidget(self.tab2.histPlot, 3, 0, 1, 4)
        if self.tab2.histTypeBox.currentText() == "General Histogram":
            self.tab2.histPlot.plotGeneralHist(self.contacts, self.tab2.attributeBox.currentText(), self.threshold, self.nsPerFrame)
        elif self.tab2.histTypeBox.currentText() == "Bin per Contact":
            self.tab2.histPlot.plotContactHist(self.contacts, self.tab2.attributeBox.currentText(), self.threshold, self.nsPerFrame,int(self.tab2.xTicksFontSizeField.text()))

        self.tab2.histPlot.update()

    def plotMap(self):
        sip.delete(self.tab3.mapPlot)
        self.tab3.mapPlot = MapPlotter(None, width=8, height=5, dpi=60)
        self.grid2.addWidget(self.tab3.mapPlot, 3, 0, 1, 4)
        if self.map1 == None or self.map2 == None or self.contacts == None or len(self.contacts) == 0:
            box = ErrorBox("Please analyze the trajectory with the resid box checked for both atom selections!")
            box.exec_()
            return
        res = self.tab3.mapPlot.plotMap(self.contacts, self.map1, self.map2,"resids 1", "resids 2",self.tab3.attributeBox.currentText(), self.threshold, self.nsPerFrame)
        if res == -1:
            box = ErrorBox("Please analyze the trajectory with the resid box checked for both atom selections!")
            box.exec_()
        self.tab3.mapPlot.update()

    def pushSave(self):
        fileName = QFileDialog.getSaveFileName(self, 'Export Path')
        self.valueUpdated.emit(fileName[0], self.tab1.formatBox.currentText())

    def setContacts(self, currentContacts):
        self.contacts = currentContacts

    def setMaps(self, map1,map2):
        self.map1 = map1
        self.map2 = map2
