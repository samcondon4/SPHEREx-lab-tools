import logging
import threading

import numpy as np
import pandas as pd
import pyqtgraph as pg
from PyQt5.QtCore import QObject, pyqtSignal
from pyqtgraph.parametertree import Parameter

import spherexlabtools.log as slt_log
from spherexlabtools.thread import QueueThread
from spherexlabtools.ui import LineViewerWidget, ImageViewerWidget

pg.setConfigOption("imageAxisOrder", "row-major")
pg.setConfigOption('useNumba', True)
logger = logging.getLogger(f"{slt_log.LOGGER_NAME}.{__name__}")


class Viewer(QueueThread, QObject):
    """ The base viewer class which performs the buffering of incoming dataframes into a larger dataframe based on the
    buffer_size attribute. Subclasses are connected to GUI interface via the widget attribute.
    """

    update = pyqtSignal(object, name='update')
    widget = None

    def __init__(self, cfg, exp, buffer_size=1, **kwargs):
        self.name = cfg['instance_name']
        self.exp = exp
        QueueThread.__init__(self)
        QObject.__init__(self)
        self.buffer = pd.DataFrame()
        self.display_object = None

        # - create parameters - #
        self.buffer_size = Parameter.create(name='Buffer Size', type='int', value=buffer_size)

    def handle(self, record):
        """ Add the latest record to the viewer buffer based on the buffer size.
        """
        cur_buffer_length = len(self.buffer.index.get_level_values(0))
        desired_buffer_length = self.buffer_size.value()
        dbuf_size = cur_buffer_length - desired_buffer_length

        if dbuf_size > 0:
            shift_ind = dbuf_size + 1
        elif dbuf_size < 0:
            shift_ind = 0
        else:
            shift_ind = 1

        append_index = pd.MultiIndex.from_product([[cur_buffer_length], np.arange(record.data.shape[0])])
        append_df = record.data.set_index(append_index)
        if cur_buffer_length > 0:
            shifted_buffer = self.buffer.loc[shift_ind:]
            new_df = pd.concat([shifted_buffer, append_df])
            new_index = pd.MultiIndex.from_tuples([(ind[0] - shift_ind, ind[1]) for ind in new_df.index])
            new_df.index = new_index
        else:
            new_df = append_df
        self.buffer = new_df

        # - update the display object and send it to the ViewerWidget - #
        self.update_display_object()
        self.update.emit(self.display_object)

    def update_display_object(self):
        """ Update the display_object attribute, which is sent out through a signal to the ViewerWidget class.
        """
        raise NotImplementedError("update_display_object() must be implemented in Viewer subclasses!")


class LineViewer(Viewer):
    """ A viewer subclass that plots data as lines on a graph. This subclass connects to the :class:`.LineViewerWidget`
    class by setting widget = LineViewerWidget.
    """

    widget = LineViewerWidget

    def __init__(self, cfg, exp, lines=None, **kwargs):
        """ Initialize a LineViewer.

        :param cfg: Configuration dictionary
        :param exp: Experiment control package
        :param lines: Dictionary of the following form: {'record column name': 'line color'}
        :param kwargs:
        """
        assert type(lines) is dict and len(lines) > 0, 'The LineViewer needs the record columns to plot!'
        super().__init__(cfg, exp, **kwargs)
        self.lines = lines
        lines_enabled_children = [None for _ in range(len(lines))]
        i = 0
        for key, val in self.lines.items():
            line_param = Parameter.create(name=key, type='bool', value=True)
            lines_enabled_children[i] = line_param
            i += 1
        self.plot_lines_enable = Parameter.create(name='Lines', type='group', children=lines_enabled_children)

        # - set the default buffer size to be larger - #
        self.buffer_size.setValue(100)
        self.buffer_size.setDefault(100)

    def update_display_object(self):
        """ Update the display object for the LineViewerWidget to plot. Sets the display object to be a dictionary of
        the following form {'line name': (data, color of the line to plot)}
        """
        self.display_object = {}
        for plot_line_param in self.plot_lines_enable.children():
            if plot_line_param.value():
                line_name = plot_line_param.name()
                display_tup = (self.buffer[line_name].values, self.lines[line_name])
                self.display_object[line_name] = display_tup


class ImageViewer(Viewer):
    """ A viewer subclass that displays 2-dimensional arrays as images. This subclass connects to the
    :class:`.ImageViewerWidget` class by setting widget = ImageViewerWidget.
    """

    widget = ImageViewerWidget

    def __init__(self, cfg, exp, **kwargs):
        super().__init__(cfg, exp, **kwargs)

    def update_display_object(self):
        """ Update the display object for the ImageViewerWidget to display. Sets the display object to the numpy values
        of the latest item in the buffer.
        """
        ind = self.buffer.index.get_level_values(0)[-1]
        img = self.buffer.loc[ind].values
        self.display_object = img
