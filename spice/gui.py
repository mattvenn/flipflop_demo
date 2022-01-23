#!/usr/bin/env python3
import sys
import csv
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

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.loadData()

        grid = QGridLayout()
        grid.addWidget(self.createGraph(), 0, 0)
        grid.addWidget(self.createControls(), 1, 0)

        self.updateGraph()

        self.schem_label = QLabel(self)
        self.measure_label = QLabel(self)
        self.measure_label.setText("0")
        grid.addWidget(self.measure_label, 2, 0)
                 
        # loading image
        self.pixmap = QPixmap('../schematic/tgff_full.png')
        self.schem_label.setPixmap(self.pixmap)
        grid.addWidget(self.schem_label, 3, 0)

        self.setWindowTitle("Wave display")
        self.setLayout(grid)
        self.resize(1800, 800)

    def loadData(self):
        print("loading data...")
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
            except FileNotFoundError as e:
                break

        self.numFiles = self.fileNumber - 1
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
        
    def createControls(self):
        groupBox = QGroupBox("Controls")
        vbox = QVBoxLayout()
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
            vbox.addWidget(box)
       
        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(10)
        slider.setMaximum(self.numFiles - 1)
        slider.setSingleStep(1)
        slider.valueChanged.connect(self.updateFile)
        vbox.addWidget(slider)

        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Window()
    gui.show()
    sys.exit(app.exec_())
