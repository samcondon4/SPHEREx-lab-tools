"""pylablib_gui_tab:

    This module implements the base class that all gui tabs inherit. This base class, GuiTab, generalizes the
    interaction with PyQt5 dialogs so that higher level software can interact with a tab in a standardized way.

Sam Condon, 06/28/2021
"""
from queue import SimpleQueue


class GuiTab:

    def __init__(self):
        self.button_queue = SimpleQueue()
        self.form = None
        self.parameters = []
        self.get_methods = {}
        self.set_methods = {}

    def get_button(self):
        """get_button: return the latest button press from the button queue

        :return: string identifying the last button that was pressed
        """
        if not self.button_queue.empty():
            button_ret = self.button_queue.get(timeout=1)
        else:
            button_ret = False

        return button_ret

    def clear_button_queue(self):
        """clear_button_queue: clear the button queue of all values

        :return: None
        """
        while not self.button_queue.empty():
            self.button_queue.get(timeout=1)

    def add_parameter(self, parameter_name, getter, setter):
        """add_parameter: add functions to the getter and setter dictionaries for the specified parameter name.

        :param parameter_name: <string> name of parameter to be added.
        :param getter: <function> function object corresponding to parameter getter.
        :param setter: <function> function object corresponding to parameter setter.
        :return: None
        """
        self.parameters.append(parameter_name)
        self.get_methods[parameter_name] = getter
        self.set_methods[parameter_name] = setter

    def get_parameters(self, params):
        """get_params: return the specified parameters as a dictionary.

        :param:
            params: string, list of strings, or "All" to specify which parameters
                    should be returned.

        :return: dictionary of the desired parameters.
        """
        return_dict = {}
        if params == 'All':
            for p in self.parameters:
                return_dict[p] = self.get_methods[p]()
        elif type(params) is list:
            for p in params:
                return_dict[p] = self.get_methods[p]()
        elif type(params) is str:
            return_dict[params] = self.get_methods[params]()

        return return_dict

    def set_parameters(self, params_dict):
        """set_params: set the specified parameters in the dialog display.

        :param params_dict: dictionary with keys and values of parameters to update
        :return: None
        """
        for key in params_dict:
            self.set_methods[key](params_dict[key])

    def place(self, tab_widget):
        """place: places the dialog specified by the inherited class into a tab widget.

        :param tab_widget: QTabWidget
        :return: None
        """
        tab_widget.addTab(self.form)

