#!/usr/bin/env python3
import sys
import csv
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider)
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

COLOURS = [
    (255, 255,   0),
    (255,   0,   0),
    (  0, 255,   0),
    (  0,   0, 255),
    (100,   0, 255),
    ] 

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.loadData()

        grid = QGridLayout()
        grid.addWidget(self.createGraph(), 0, 0)
        grid.addWidget(self.createControls(), 1, 0)
        self.setLayout(grid)

        self.updateGraph(0)

        self.setWindowTitle("Wave display")
        self.resize(1800, 800)

    def loadData(self):
        fileNumber = 1 
        self.data = []
        while True:
            try:
                with open('csv/%d' % fileNumber) as f:
                    reader = csv.DictReader(f, delimiter=' ', skipinitialspace=True)
                    self.nodeNames = reader.fieldnames

                    self.data.append({})
                    for nodeName in self.nodeNames:
                        self.data[fileNumber-1][nodeName] = []

                    for row in reader:
                        for nodeName in self.nodeNames:
                            self.data[fileNumber-1][nodeName].append(float(row[nodeName]))

                fileNumber += 1
            except FileNotFoundError as e:
                break
            if fileNumber > 100:
                break

        self.numFiles = fileNumber - 1
        print("Loaded %d records" % fileNumber)
        print("Nodenames: %s" % self.nodeNames)

    # setup the graph widgets - no data yet
    def createGraph(self):
        graphWidget = pg.PlotWidget()
        self.graphs = {}
        width = 2
        colourNum = 0
        for nodeName in self.nodeNames:
            pen = pg.mkPen(color=COLOURS[colourNum], width=width)
            self.graphs[nodeName] = graphWidget.plot(pen=pen)
            colourNum += 1

        graphWidget.setYRange(0, 2, padding=0)
        return graphWidget

    # when slider is moved, update data
    def updateGraph(self, fileNumber):
        # for each node read, update its graph
        for nodeName in self.nodeNames:
            if nodeName == 'time':
                continue
            if self.showControls[nodeName].isChecked():
                self.graphs[nodeName].setData(self.data[fileNumber]['time'], self.data[fileNumber][nodeName])
            else:
                self.graphs[nodeName].clear()
        
    def createControls(self):
        groupBox = QGroupBox("Controls")
        vbox = QVBoxLayout()
        self.showControls = {}
        for nodeName in self.nodeNames:
            if nodeName == 'time':
                continue
            box = QCheckBox(nodeName)
            box.setChecked(True)
            self.showControls[nodeName] = box
            vbox.addWidget(box)

        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(10)
        slider.setMaximum(self.numFiles - 1)
        slider.setSingleStep(1)
        slider.valueChanged.connect(self.updateGraph)
        vbox.addWidget(slider)

        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Window()
    gui.show()
    sys.exit(app.exec_())
