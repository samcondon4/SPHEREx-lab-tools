import sys
import asyncio
import qasync
from PyQt5.QtWidgets import *
sys.path.append('..\\pylabcal\\pylabcalgui\\CS260-Window')
sys.path.append('..\\pylablib\\instruments')
sys.path.append('Transmission-Measurement')
from cs260_dialog_mainwindow import *
import transmission_measurement_main

transmission = True

class PylabMiscDialog(CS260Window):
    def __init__(self, cs, sync_queue, transmission=False):
        super().__init__(cs, sync_queue=sync_queue)
        if transmission is True:
            transmission_measurement_main.add_transmission_tab(self.ui.tabWidget)


if __name__ == "__main__":
    # Create cs260 control instance and synchronization queue
    exe_path = "..\\pylablib\\instruments\\CS260-Drivers\\C++EXE.exe"
    cs = CS260(exe_path)
    sync_queue = asyncio.Queue()

    app = QApplication(sys.argv)
    loop = QEventLoop()
    asyncio.set_event_loop(loop)
    main_dialog = PylabMiscDialog(cs, sync_queue, transmission=transmission)
    main_dialog.show()
    with loop:
        loop.run_forever()
        loop.close()
    cs.close()
    sys.exit(app.exec_())










