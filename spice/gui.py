#!/usr/bin/env python3
import sys
import csv
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider)
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.loadData()

        grid = QGridLayout()
        grid.addWidget(self.createGraph(), 0, 0)
        grid.addWidget(self.createControls(), 1, 0)
        self.setLayout(grid)

        self.setWindowTitle("Wave display")
        self.resize(1800, 800)

    def loadData(self):
        filenumber = 1 
        self.data = []
        while True:
            try:
                with open('csv/%d' % filenumber) as f:
                    self.data.append( [d[0:-1] for d in csv.reader(f, delimiter=' ', skipinitialspace=True)] )
                filenumber += 1
            except FileNotFoundError as e:
                break
        print("loaded %d records" % filenumber)
        print("CSV header: %s" % self.data[0][0])
        print("time points in record: %d" % len(self.data[0]))

        self.dataLabels = self.data[0][0][1:]
        self.numFiles = len(self.data)

    # setup the graph widgets - no data yet
    def createGraph(self):
        graphWidget = pg.PlotWidget()
        width = 2
        pen = pg.mkPen(color=(255, 0, 0), width=width)
        self.data1 = graphWidget.plot(pen=pen)
        pen = pg.mkPen(color=(0, 255, 0), width=width)
        self.data2 = graphWidget.plot(pen=pen)
        pen = pg.mkPen(color=(0, 0, 255), width=width)
        self.data3 = graphWidget.plot(pen=pen)

        graphWidget.setYRange(0, 2, padding=0)
        return graphWidget

    # when slider is moved, update data
    def updateGraph(self, filenumber):
        a = []
        b = []
        c = []
        x = []
        for row in self.data[filenumber][1:]:
            x.append(float(row[0]))
            a.append(float(row[1]))
            b.append(float(row[2]))
            c.append(float(row[3]))

        self.data1.setData(x, a)
        self.data2.setData(x, b)
        self.data3.setData(x, c)
        
    def createControls(self):
        groupBox = QGroupBox("Controls")
        vbox = QVBoxLayout()

        for label in self.dataLabels:
            box1 = QCheckBox(label)
            box1.setChecked(True)
            vbox.addWidget(box1)

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
