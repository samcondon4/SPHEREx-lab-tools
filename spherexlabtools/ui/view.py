import pyqtgraph as pg
from PyQt5 import QtWidgets


class ViewerWidget(QtWidgets.QWidget):

    def __init__(self, name=None, **kwargs):
        QtWidgets.QWidget.__init__(self, **kwargs)
        self.name = name
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.graphics_layout = pg.GraphicsLayoutWidget()
        self.layout.addWidget(self.graphics_layout)

    def update(self, *args, **kwargs):
        """ This is the main method of the ViewerWidgets which update the graphical elements
        of the display. Must be implemented in subclasses.
        """
        raise NotImplementedError('update() must be implemented in a ViewerWidget subclass!')


class LineViewerWidget(ViewerWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plot_item = self.graphics_layout.addPlot(row=0, col=0)
        self.legend_item = self.plot_item.addLegend()

    def update(self, plot_dict):
        """ Updates the plot_item in the graphics layout with data transferred in the plot_dict.

        :param plot_dict: Dictionary of the following form: {'name of line': ([array of data], 'color of the line')}
        """
        pass


class ImageViewerWidget(ViewerWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.view = self.graphics_layout.addViewBox()
        self.view.setAspectLocked(True)
        self.img = pg.ImageItem(border='w')
        self.view.addItem(self.img)

    def update(self):
        pass
