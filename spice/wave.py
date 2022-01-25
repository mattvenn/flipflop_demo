#!/usr/bin/env python3
import sys
import csv
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

ALIASES = {
    'Xflop.a_27_47#'    : 'CLK_INV',
    'Xflop.a_193_47#'   : 'CLK_INV_INV',
    'Xflop.a_381_47#'   : 'D_INV',
    'Xflop.a_466_413#'  : 'X2_IN',
    'Xflop.a_634_159#'  : 'X2_OUT',
    }

# https://colorswall.com/palette/73/
COLOURS = [
    (0xff,0xf1,0x00), 
    (0xff,0x8c,0x00), # Q
    (0xe8,0x11,0x23), # D
    (0xec,0x00,0x8c), # clk
    (0x68,0x21,0x7a), # clk in
    (0x00,0x18,0x8f), # clk inv inv
    (0x00,0xbc,0xf2), # d inv
    (0x00,0xb2,0x94), # x2 in
    (0x00,0x9e,0x49), # x2 out
    (0xba,0xd8,0x0a),
    (0xff,0xf1,0x00),
    ] 

PEN_WIDTH = 3

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        uic.loadUi('ui/wave.ui', self)

        self.loadData()
        self.graph_layout.addWidget(self.createGraph())
        self.addCheckboxes()
        self.updateGraph()
                 
        # loading image
        self.pixmap = QPixmap('../schematic/tgff_with_clock.png')
        self.schem_label.setPixmap(self.pixmap)
        self.setWindowTitle("Wave display")

    def loadData(self):
        print("loading data", end='')
        self.fileNumber = 1 
        self.data = []
        while True:
            try:
                with open('csv/%d' % self.fileNumber) as f:
                    reader = csv.DictReader(f, delimiter=' ', skipinitialspace=True)
                    self.nodeNames = reader.fieldnames
                    # sometimes it reads an extra empty fieldname
                    if '' in self.nodeNames:
                        self.nodeNames.remove('')

                    self.data.append({})
                    for nodeName in self.nodeNames:
                        self.data[self.fileNumber-1][nodeName] = []

                    for row in reader:
                        for nodeName in self.nodeNames:
                            self.data[self.fileNumber-1][nodeName].append(float(row[nodeName]))

                self.fileNumber += 1
                if self.fileNumber % 10 == 0:
                    print(".", end='', flush=True)
            except FileNotFoundError as e:
                break


        self.numFiles = self.fileNumber - 1
        print("")
        print("Loaded %d records" % self.fileNumber)
        print("Nodenames: %s" % self.nodeNames)
        self.fileNumber = 0

    def update_line(self, line):
        delta = self.line_1.value() - self.line_2.value()
        delta *= 1e12
        self.measure_label.setText("delta = %d ps" % delta)

    # setup the graph widgets - no data yet
    def createGraph(self):
        graphWidget = pg.PlotWidget()
        self.graphs = {}
        for num, nodeName in enumerate(self.nodeNames):
            pen = pg.mkPen(color=COLOURS[num], width=PEN_WIDTH)
            self.graphs[nodeName] = graphWidget.plot(pen=pen)

        graphWidget.setYRange(0, 1.8, padding=0.2)
        graphWidget.showGrid(x = True, y = True, alpha = 0.7) 

        self.line_1 = graphWidget.addLine(x=0, movable=True, pen=pen)
        self.line_2 = graphWidget.addLine(x=0, movable=True, pen=pen)
        self.line_1.sigPositionChanged.connect(self.update_line)
        self.line_2.sigPositionChanged.connect(self.update_line)
        return graphWidget

    def updateFile(self, number):
        self.fileNumber = number
        self.updateGraph()

    # when slider is moved, update data
    def updateGraph(self):
        # for each node read, update its graph
        for nodeName in self.nodeNames:
            if nodeName == 'time':
                continue
            if self.showControls[nodeName].isChecked():
                self.graphs[nodeName].setData(self.data[self.fileNumber]['time'], self.data[self.fileNumber][nodeName])
            else:
                self.graphs[nodeName].clear()
        
    def addCheckboxes(self):
        self.showControls = {}
        for num, nodeName in enumerate(self.nodeNames):
            if nodeName == 'time':
                continue

            if nodeName in ALIASES:
                box = QCheckBox(ALIASES[nodeName])
            else:
                box = QCheckBox(nodeName)

            if num <= 3:
                box.setChecked(True)
            box.stateChanged.connect(self.updateGraph)
            box.setStyleSheet("background:rgb(%d,%d,%d);" % (COLOURS[num][0], COLOURS[num][1], COLOURS[num][2]))
            self.showControls[nodeName] = box
            self.checkbox_layout.addWidget(box)
       
        # slider config
        self.slider.setMaximum(self.numFiles - 1)
        self.slider.valueChanged.connect(self.updateFile)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
