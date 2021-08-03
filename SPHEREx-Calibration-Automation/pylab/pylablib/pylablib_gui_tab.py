"""pylablib_gui_tab:

    This module implements the base class that all gui tabs inherit. This base class, GuiTab, generalizes the
    interaction with PyQt5 dialogs so that higher level software can interact with a tab in a standardized way.

Sam Condon, 06/28/2021
"""
from queue import SimpleQueue
from PyQt5 import QtWidgets
from pylablib.QListWigetSubclass import QListWidgetItemCustom


class GuiTab:

    # Queue object that can be shared if multiple GuiTabs should share the same namespace #
    GlobalButtonQueue = SimpleQueue()
    #######################################################################################

    @classmethod
    def get_global_button(cls):
        """get_global_button: return the latest button press from the global queue

        :return: string identifying the last button that was pressed
        """
        if not cls.GlobalButtonQueue.empty():
            button_ret = cls.GlobalButtonQueue.get(timeout=1)
        else:
            button_ret = False
        return button_ret

    @classmethod
    def clear_global_button_queue(cls):
        """clear_button_queue: clear the global button queue of all values

        :return: None
        """
        while not cls.GlobalButtonQueue.empty():
            cls.GlobalButtonQueue.get(timeout=1)

    @classmethod
    def add_item_to_list(cls, item_list, text, data, role=0):
        """add_item_to_list: Add an item to the given list.

            item_list: QListWidget to add the item to.
            text: item text string.
            data: item data.
            role: item role. Most of the time this argument can be ignored.
        """
        list_item = QListWidgetItemCustom()
        list_item.setData(role, data)
        list_item.setText(text)
        list_item.set_user_data(data)

        item_list.addItem(list_item)

    @classmethod
    def remove_item_from_list(cls, item_list):
        """remove_item_from_list: Remove the currently selected item from the given list.
        """
        rem_item = item_list.currentItem()
        if rem_item is not None:
            rem_row = item_list.currentRow()
            item_list.takeItem(rem_row)

    @classmethod
    def remove_all_items_from_list(cls, item_list):
        """remove_all_items_from_list: Remove all items from the given list.
        """
        item_list.clear()

    def __init__(self, child):
        self.form = None
        self.window_selector_dict = None
        self.button_queue = SimpleQueue()
        self.parameters = []
        self.get_methods = {}
        self.set_methods = {}
        self.child = child

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

    def configure_stacked_widget_switch(self):
        """configure_stacked_widget_switch: Stacked widgets do not naturally provide any means of switching between
                                            the tabs that have been added. This method builds a dropdown menu to switch
                                            between the windows of a stacked widget.

        params: None
        return: None
        """
        widget_list = [self.form.widget(i) for i in range(self.form.count())]
        self.window_selector_dict = {}
        for widget in widget_list:
            window_selector = QtWidgets.QComboBox()
            widget_name = widget.windowTitle()
            layout = widget.layout()
            for w in widget_list:
                window_selector.addItem(w.windowTitle())
            window_selector.currentIndexChanged.connect(self._on_stacked_widget_select)
            layout.addWidget(window_selector, 0, layout.columnCount() - 1)
            widget.setLayout(layout)
            self.window_selector_dict[widget_name] = window_selector

    # Stacked widget switching #
    def _on_stacked_widget_select(self):
        """_on_stacked_widget_select: Change the stacked widget window according to the combo box window selector
        """
        cur_window = self.form.currentWidget().windowTitle()
        new_index = self.window_selector_dict[cur_window].currentIndex()
        self.form.setCurrentIndex(new_index)
        new_window = self.form.currentWidget().windowTitle()
        self.window_selector_dict[new_window].setCurrentIndex(new_index)

