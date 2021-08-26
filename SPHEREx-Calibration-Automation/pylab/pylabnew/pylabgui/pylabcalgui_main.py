"""GUI:

    This module provides the top level wrapper class for the SPHEREx Test and Calibration Graphical User Interface

Sam Condon, 08/14/2021
"""

import asyncio
from qasync import QEventLoop
from PyQt5 import QtWidgets
from pylabgui.pylabgui_window_base import GuiCompositeWindow
from pylabgui.pylabcalgui_automationTab import AutoTab
from pylabgui.pylabcalgui_manualTab import ManualTab


class GUI(GuiCompositeWindow):

    def __init__(self, sequence_dir=None, data_queues=None):
        super().__init__(child=self, window_type="tab")
        self.proc_queue = asyncio.Queue()
        if data_queues is None:
            queue_list = [self.proc_queue]
            self.standalone = True
        else:
            queue_list = data_queues
            self.standalone = False
        self.auto = AutoTab(sequence_dir=sequence_dir, data_queues=queue_list)
        self.manual = ManualTab(data_queues=queue_list)
        self.add_widget(self.auto.form)
        self.add_widget(self.manual.form)
        if not self.configured:
            self.configure()

    async def run(self):
        """run: main method to run the PyQt5 GUI.
        """
        # Start Tab Execution ###########################################
        manual_task = asyncio.create_task(self.manual.run())
        auto_task = asyncio.create_task(self.auto.run())
        #################################################################
        while True:
            if self.standalone:
                gui_data = await self.proc_queue.get()
                print(gui_data)
            else:
                break
        await asyncio.gather(manual_task, auto_task)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    event_loop = QEventLoop()
    asyncio.set_event_loop(event_loop)
    seq_dir = "..\\config\\sequence\\"
    window = GUI(seq_dir)
    window.form.show()
    asyncio.create_task(window.run())
    with event_loop:
        event_loop.run_forever()
        event_loop.close()
    sys.exit(app.exec_())
