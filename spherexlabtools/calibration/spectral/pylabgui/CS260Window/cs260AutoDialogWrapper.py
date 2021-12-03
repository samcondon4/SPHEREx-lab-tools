"""cs260AutoDialogWrapper:

    This module provides a wrapper class, CS260AutoWindow, around the cs260AutoDialog that
    was generated using QT-Designer.

Sam Condon, 08/16/2021
"""

from PyQt5 import QtWidgets
from .cs260AutoDialog import Ui_Form
from ..pylabgui_window_base import GuiWindow


class CS260AutoWindow(Ui_Form, GuiWindow):

    def __init__(self, **kwargs):
        super().__init__(child=self, **kwargs)
        self.setupUi(self.form)
        if not self.configured:
            self.configure()
        self.WidgetGroups["cs260_grating_transitions"].set_list_setter_proc(self.grating_transition_listitem_proc)
        self.WidgetGroups["cs260_osf_transitions"].set_list_setter_proc(self.osf_transition_listitem_proc)

    @staticmethod
    def grating_transition_listitem_proc(grating_transition):
        """ Grating transition processing for updating the list from the saved_sequences group.
        """
        wavelength = float(grating_transition["wavelength"])
        grating = int(grating_transition["grating"])
        text = "wavelength = %f, grating = %i" % (wavelength, grating)
        data = {"wavelength": wavelength, "grating": grating}
        return text, data

    @staticmethod
    def osf_transition_listitem_proc(osf_transition):
        """ Order sort filter transition processing for updating the list from the saved_sequences group.
        """
        wavelength = float(osf_transition["wavelength"])
        osf = int(osf_transition["osf"])
        text = "wavelength = %f, osf = %i" % (wavelength, osf)
        data = {"wavelength": wavelength, "osf": osf}
        return text, data


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CS260AutoWindow()
    window.form.show()
    sys.exit(app.exec_())
