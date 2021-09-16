"""manualTab:

    This module ties together all of the manual instrument control windows into a single QtWidget

Sam Condon, 08/09/2021
"""

from pylabgui.CS260Window.cs260DialogWrapper import CS260Window
from pylabgui.LockinWindow.lockinWindowDialogWrapper import *
from pylabgui.NDFWheelWindow.ndfWheelDialogWrapper import NDFWindow
from pylabgui.LabJackWindow.labjackWindowDialogWrapper import LabjackWindow


class ManualTab(GuiCompositeWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, window_type="stacked", **kwargs)
        self.form.setWindowTitle("Manual")
        self.proc_queue = asyncio.Queue()
        self.cs260_window = CS260Window(rx_identifier="CS260", debug=True, **kwargs)
        self.lockin_window = LockinWindow(**kwargs)
        self.ndf_window = NDFWindow(rx_identifier="NDF", **kwargs)
        self.labjack_window = LabjackWindow(rx_identifier="LABJACK", **kwargs)
        self.add_window(self.cs260_window)
        self.add_window(self.lockin_window)
        self.add_window(self.ndf_window)
        self.add_window(self.labjack_window)
        if not self.configured:
            self.configure()


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
