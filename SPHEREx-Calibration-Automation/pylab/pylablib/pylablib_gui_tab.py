"""pylablib_gui_tab:

    This module implements the base class that all gui tabs inherit. This base class, GuiTab, generalizes the
    interaction with PyQt5 dialogs so that higher level software can interact with a tab in a standardized way.

Sam Condon, 06/28/2021
"""
from queue import SimpleQueue
from PyQt5 import QtWidgets


class GuiTab:

    def __init__(self, child):
        self.button_queue = SimpleQueue()
        self.parameters = []
        self.get_methods = {}
        self.set_methods = {}
        self.child = child
        # Configure stacked widget switching #########################################################
        try:
            is_stacked = child.is_stacked_widget
        except AttributeError as e:
            pass
        else:
            if is_stacked:
                widget_list = [child.stackedWidget.widget(i) for i in range(child.stackedWidget.count())]
                self.window_selector_dict = {}
                for widget in widget_list:
                    window_selector = QtWidgets.QComboBox()
                    widget_name = widget.objectName()
                    layout = widget.layout()
                    for w in widget_list:
                        window_selector.addItem(w.objectName())
                    window_selector.currentIndexChanged.connect(self._on_stacked_widget_select)
                    layout.addWidget(window_selector, 0, layout.columnCount() - 1)
                    widget.setLayout(layout)
                    self.window_selector_dict[widget_name] = window_selector
        ###############################################################################################

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
        if "parameter_name" not in self.parameters:
            self.parameters.append(parameter_name)
        self.get_methods[parameter_name] = getter
        self.set_methods[parameter_name] = setter

    def add_set_parameter(self, parameter_name, setter):
        """add_set_parameter: add a function to the setter dictionary for the specified parameter name.

        """
        if parameter_name not in self.parameters:
            self.parameters.append(parameter_name)
        self.set_methods[parameter_name] = setter

    def add_get_parameter(self, parameter_name, getter):
        """add_set_parameter: add a function to the getter dictionary for the specified parameter name.

        """
        if parameter_name not in self.parameters:
            self.parameters.append(parameter_name)
        self.set_methods[parameter_name] = getter

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

    # Stacked widget switching #
    def _on_stacked_widget_select(self):
        """_on_stacked_widget_select: Change the stacked widget window according to the combo box window selector
        """
        cur_window = self.child.stackedWidget.currentWidget().objectName()
        new_index = self.child.window_selector_dict[cur_window].currentIndex()
        self.child.stackedWidget.setCurrentIndex(new_index)
        new_window = self.child.stackedWidget.currentWidget().objectName()
        self.window_selector_dict[new_window].setCurrentIndex(new_index)

