"""lockinAutoWindowDialogWrapper:

    This module provides a wrapper class, LockinAutoWindow, around the lockinAutoWindowDialogWrapper class that
    was generated using QT-Designer.

Sam Condon, 08/14/2021
"""

from PyQt5 import QtWidgets
from pylabgui.LockinWindow.sr830AutoDialog import Ui_Form
from pylabgui.LockinWindow.lockinWindowHelper import Lockin
from pylabgui.pylabgui_window_base import GuiWindow


class Sr830AutoWindow(Ui_Form, Lockin, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()
        self.WidgetGroups["sr830 sens transitions"].set_list_setter_proc(self.lockin_sens_transition_listitem_proc)

    def lockin_sens_transition_listitem_proc(self, sens_transition):
        get_sens_dict = {"value": None, "multiplier": None, "units": None}
        for key in sens_transition:
            if "value" in key:
                get_sens_dict["value"] = sens_transition[key]
            elif "multiplier" in key:
                get_sens_dict["multiplier"] = sens_transition[key]
            elif "units" in key:
                get_sens_dict["units"] = sens_transition[key]
        wavelength = sens_transition["wavelength"]
        sens_dict = self.get_sensitivity(get_sens_dict)
        sens_data = {"wavelength": sens_transition["wavelength"], "sensitivity": sens_dict["sensitivity"]}
        sens_text = "{}{}".format(sens_dict["sensitivity"]/sens_dict["unit_multiplier"], get_sens_dict["units"])
        text = "wavelength = {}, sensitivity = {};".format(wavelength, sens_text)
        return text, sens_data


"""
class LockinAutoWindow(Lockin, Ui_Form, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()
        # Add list item proc method
        self.WidgetGroups["sr510 sens transitions"].set_list_setter_proc(self.lockin_sens_transition_listitem_proc)
        self.WidgetGroups["sr830 sens transitions"].set_list_setter_proc(self.lockin_sens_transition_listitem_proc)

    def lockin_sens_transition_listitem_proc(self, sens_transition):
        get_sens_dict = {"value": None, "multiplier": None, "units": None}
        for key in sens_transition:
            if "value" in key:
                get_sens_dict["value"] = sens_transition[key]
            elif "multiplier" in key:
                get_sens_dict["multiplier"] = sens_transition[key]
            elif "units" in key:
                get_sens_dict["units"] = sens_transition[key]
        wavelength = sens_transition["wavelength"]
        sens_dict = self.get_sensitivity(get_sens_dict)
        sens_data = {"wavelength": sens_transition["wavelength"], "sensitivity": sens_dict["sensitivity"]}
        sens_text = "{}{}".format(sens_dict["sensitivity"]/sens_dict["unit_multiplier"], get_sens_dict["units"])
        text = "wavelength = {}, sensitivity = {};".format(wavelength, sens_text)
        return text, sens_data


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = LockinAutoWindow()
    window.form.show()
    sys.exit(app.exec_())
"""
