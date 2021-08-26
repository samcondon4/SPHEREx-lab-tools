import sys
import asyncio
import numpy as np
import time
from qasync import QEventLoop
from PyQt5 import QtWidgets
from powermaxLiveWindowDialogWrapper import PowermaxWindow


async def function_gen(powermax_window):
    acquisition = False
    iter = 0
    while True:
        button = powermax_window.get_button()
        if button is not False:
            print(button)

        if button == "Start Acquisition":
            acquisition = True
        elif button == "Stop Acquisition":
            acquisition = False

        if acquisition:
            # Append data to display. This will of course be replaced with real data from the powermax usb sensor! ##
            data = np.random.randn()
            if iter > 100:
                data += 10
            powermax_window.set_parameters({"data append": data})
            iter += 1
            #########################################################################################################

        await asyncio.sleep(0.01)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PowermaxWindow()
    event_loop = QEventLoop()
    asyncio.set_event_loop(event_loop)
    window.form.show()
    asyncio.create_task(function_gen(window))
    with event_loop:
        event_loop.run_forever()
        event_loop.close()
    sys.exit(app.exec_())
