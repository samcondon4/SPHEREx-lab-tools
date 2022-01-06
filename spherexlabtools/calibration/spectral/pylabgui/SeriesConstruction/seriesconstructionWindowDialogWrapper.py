"""seriesConstructionWindowDialogWrapper:

    This module provides a wrapper class, SeriesConstructionWindow, around the seriesConstructionWindowDialog that
    was generated using QT-Designer.

Sam Condon, 08/14/2021
"""

from PyQt5 import QtWidgets
from ..pylabgui_window_base import GuiWindow
from .seriesconstructionWindowDialog import Ui_Form


class SeriesConstructionWindow(Ui_Form, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()

        # add setter_proc method to create a dictionary for the thorlabs detectors.
        # TODO: MOVE THORLABS DETECTORS TO THEIR OWN GUI WINDOW, THIS IS NOT A GOOD WAY OF DOING THIS...
        #self.WidgetGroups["saved_sequences"].set_list_setter_proc(lambda passive_data: print(passive_data))

        # window specific configuration #
        if self.data_queue_tx is not None:
            self.AbortSeriesButton.clicked.connect(self.abort_series)
            self.PauseSeriesButton.clicked.connect(self.pause_series)

    def abort_series(self):
        """ Place an "abort" message on the tx data queue.
        """
        self.data_queue_tx.put_nowait("abort")

    def pause_series(self):
        """ Place a "pause" message on the tx data queue.
        """
        self.data_queue_tx.put_nowait("pause")
    #################################################################################################################


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    sequence_dir = ".\\sequences\\seriesConstructionWindowTest\\"
    window = SeriesConstructionWindow()
    window.form.show()
    sys.exit(app.exec_())
