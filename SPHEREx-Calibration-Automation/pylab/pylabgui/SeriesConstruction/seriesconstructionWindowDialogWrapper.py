"""seriesConstructionWindowDialogWrapper:

    This module provides a wrapper class, SeriesConstructionWindow, around the seriesConstructionWindowDialog that
    was generated using QT-Designer.

Sam Condon, 08/14/2021
"""

import asyncio
from PyQt5 import QtWidgets
from pylabgui.SeriesConstruction.seriesconstructionWindowDialog import Ui_Form
from pylabgui.pylabgui_window_base import GuiWindow


class SeriesConstructionWindow(Ui_Form, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()

        # window specific configuration #
        if self.data_queue_tx is not None:
            self.AbortSeriesButton.clicked.connect(self.start_abort_series)
            self.PauseResumeSeriesButton.clicked.connect(self.start_pause_resume_series)

    def start_abort_series(self):
        """ start the abort_series gui coroutine.
        """
        asyncio.create_task(self.abort_series())

    async def abort_series(self):
        """ Place an "abort" message on the tx data queue and wait for a response on the rx queue indicating a
            successful or failed abort.
        """
        self.data_queue_tx.put_nowait("abort")

    def start_pause_resume_series(self):
        """ start the pause/resume series gui coroutine.
        """
        pass

    async def pause_resume_series(self):
        """ Place a "pause" or "resume" message on the tx data queue and wait for a response on the rx queue to indicate
            a successful or failed pause or resume.
        """
        pass
    #################################################################################################################


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    sequence_dir = ".\\sequences\\seriesConstructionWindowTest\\"
    window = SeriesConstructionWindow()
    window.form.show()
    sys.exit(app.exec_())
