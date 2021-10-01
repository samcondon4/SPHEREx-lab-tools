"""GUI:

    This module provides the top level wrapper class for the SPHEREx Test and Calibration Graphical User Interface

Sam Condon, 08/14/2021
"""

import asyncio
from qasync import QEventLoop
from PyQt5 import QtWidgets
from .pylabgui_window_base import GuiCompositeWindow
from .pylabcalgui_automationTab import AutoTab
from .pylabcalgui_manualTab import ManualTab


class GUI(GuiCompositeWindow):

    def __init__(self, sequence_dir=None, **kwargs):
        super().__init__(child=self, window_type="tab", **kwargs)
        self.auto = AutoTab(sequence_dir=sequence_dir, **kwargs)
        self.manual = ManualTab(**kwargs)
        self.add_window(self.auto)
        self.add_window(self.manual)
        if not self.configured:
            self.configure()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    event_loop = QEventLoop()
    asyncio.set_event_loop(event_loop)
    if len(sys.argv) > 1: 
        seq_dir = sys.argv[1] 
    else:
        seq_dir = None
    tx_queue = asyncio.Queue()
    rx_queue = asyncio.Queue()
    window = GUI(seq_dir, data_queue_tx=tx_queue, data_queue_rx=rx_queue)
    window.form.show()
    #asyncio.create_task(window.standalone_run())
    with event_loop:
        event_loop.run_forever()
        event_loop.close()
    sys.exit(app.exec_())
