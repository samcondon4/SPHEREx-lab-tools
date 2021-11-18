"""lockinAutoWindowDialogWrapper:

    This module provides a wrapper class, LockinAutoWindow, around the lockinAutoWindowDialogWrapper class that
    was generated using QT-Designer.

Sam Condon, 08/14/2021
"""

from PyQt5 import QtWidgets
from pylabgui.LockinWindow.sr510AutoDialog import Ui_Sr510
from pylabgui.LockinWindow.sr830AutoDialog import Ui_Sr830
from pylabgui.LockinWindow.lockinWindowHelper import Lockin
from pylabgui.pylabgui_window_base import GuiWindow, GuiCompositeWindow


def lockin_sens_transition_listitem_proc(sens_transition):
    """

    :param sens_transition:
    :return:
    """

    get_sens_dict = {"value": None, "multiplier": None, "units": None}
    for key in sens_transition:
        if "value" in key:
            get_sens_dict["value"] = sens_transition[key]
        elif "multiplier" in key:
            get_sens_dict["multiplier"] = sens_transition[key]
        elif "units" in key:
            get_sens_dict["units"] = sens_transition[key]
    wavelength = sens_transition["wavelength"]
    sens_dict = Lockin.get_sensitivity(get_sens_dict)
    sens_data = {"wavelength": sens_transition["wavelength"], "sensitivity": sens_dict["sensitivity"]}
    sens_text = str(sens_dict["sensitivity"])
    text = "wavelength = {}, sensitivity = {};".format(wavelength, sens_text)
    return text, sens_data


class Sr510AutoWindow(Ui_Sr510, Lockin, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()
        self.WidgetGroups["sr510_sens_transitions"].set_list_setter_proc(lockin_sens_transition_listitem_proc)


class Sr830AutoWindow(Ui_Sr830, Lockin, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()
        self.WidgetGroups["sr830_sens_transitions"].set_list_setter_proc(lockin_sens_transition_listitem_proc)


class LockinAutoWindow(Lockin, GuiCompositeWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, window_type="tab", **kwargs)
        if "identifier" in list(kwargs.keys()):
            kwargs.pop("identifier")
        self.sr510_auto_window = Sr510AutoWindow(rx_identifier="SR510 Auto")
        self.sr830_auto_window = Sr830AutoWindow(rx_identifier="SR830 Auto")
        self.add_window(self.sr510_auto_window)
        self.add_window(self.sr830_auto_window)
        self.form.setWindowTitle("Lock-in Amplifiers")
        if not self.configured:
            self.configure()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = LockinAutoWindow()
    window.form.show()
    sys.exit(app.exec_())
