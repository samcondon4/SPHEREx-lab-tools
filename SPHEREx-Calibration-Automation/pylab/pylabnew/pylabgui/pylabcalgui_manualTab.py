"""manualTab:

    This module ties together all of the manual instrument control windows into a single QtWidget

Sam Condon, 08/09/2021
"""


import asyncio
from qasync import QEventLoop
from PyQt5 import QtWidgets
from pylablib.pylablibgui_window_base import GuiCompositeWindow
from pylabcal.pylabcalgui.CS260Window.cs260DialogWrapper import CS260Window
from pylabcal.pylabcalgui.LockinWindow.lockinWindowDialogWrapper import LockinWindow
from pylabcal.pylabcalgui.NDFWheelWindow.ndfWheelDialogWrapper import NDFWindow
from pylabcal.pylabcalgui.LabJackWindow.labjackWindowDialogWrapper import LabjackWindow


class ManualTab(GuiCompositeWindow):

    def __init__(self, data_queues=None):
        super().__init__(child=self, window_type="stacked")
        self.form.setWindowTitle("Manual")
        self.proc_queue = asyncio.Queue()
        if data_queues is None:
            queue_list = [self.proc_queue]
            self.standalone = True
        else:
            queue_list = data_queues
            self.standalone = False
        self.cs260_window = CS260Window(data_queues=queue_list)
        self.lockin_window = LockinWindow(data_queues=queue_list)
        self.ndf_window = NDFWindow(data_queues=queue_list)
        self.labjack_window = LabjackWindow(data_queues=queue_list)
        self.add_widget(self.cs260_window.form)
        self.add_widget(self.lockin_window.form)
        self.add_widget(self.ndf_window.form)
        self.add_widget(self.labjack_window.form)
        if not self.configured:
            self.configure()

    async def run(self):
        """run: Coroutine to run the manual tab gui window, this is mainly used for debugging purposes.
        """
        # Initialize GUI run tasks ######################################
        asyncio.create_task(self.lockin_window.run())
        #################################################################
        while True:
            if self.standalone:
                gui_data = await self.proc_queue.get()
                print("##### ManualTab Queue Data Received ########")
                print(gui_data)
            else:
                break


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EventLoop = QEventLoop()
    asyncio.set_event_loop(EventLoop)
    window = ManualTab()
    window.form.show()
    asyncio.create_task(window.run())
    with EventLoop:
        EventLoop.run_forever()
        EventLoop.close()
    sys.exit(app.exec_())
