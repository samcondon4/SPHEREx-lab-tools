"""pylablib_gui_tab:

    This module implements the base class that all gui tabs inherit. This base class, GuiTab, generalizes the
    interaction with PyQt5 dialogs so that higher level software can interact with a tab in a standardized way.

Sam Condon, 06/28/2021
"""
from queue import SimpleQueue
from PyQt5 import QtWidgets
from pylablib.QListWigetSubclass import QListWidgetItemCustom


# Miscellaneous helper functions ################################################################
def flatten_list(in_list):
    flist = []
    [flist.extend(flatten_list(e)) if type(e) is list else flist.extend([e]) for e in in_list]
    return flist
#################################################################################################


class GuiTab:

    ButtonQueues = {}
    Buttons = []

    @classmethod
    def add_button_queue(cls, key):
        """add_button_queue: Add a new button queue with the specified key
        """
        queue = SimpleQueue()
        cls.ButtonQueues[key] = queue

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

    def __init__(self, child, button_queue_keys=None):
        # super().__init__(self)
        if button_queue_keys is None:
            self.button_queue_keys = []
        else:
            self.button_queue_keys = button_queue_keys
        self.child = child
        self.window_selector_dict = None
        self.parameters = []
        self.get_methods = {}
        self.set_methods = {}

        self.configure_button_queues()

    def configure_button_queues(self):
        """configure_button_queues: Configure all buttons in a widget to update the button queues that a GuiTab instance
                                    has access to.
        """
        widgets = self.get_widgets_from_layout(self.child.form.layout())
        for w in widgets:
            if type(w) is QtWidgets.QWidgetItem:
                widget = w.widget()
            else:
                widget = w
            if type(widget) is QtWidgets.QPushButton and widget not in GuiTab.Buttons:
                GuiTab.Buttons.extend([widget])
                widget.clicked.connect(lambda state, in_widget=widget: self.add_button_to_queues(in_widget))

    def configure_stacked_widget_switch(self):
        """configure_stacked_widget_switch: Stacked widgets do not naturally provide any means of switching between
                                            the tabs that have been added. This method builds a dropdown menu to switch
                                            between the windows of a stacked widget.

        params: None
        return: None
        """
        widget_list = [self.child.form.widget(i) for i in range(self.child.form.count())]
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

    def get_button(self, key):
        """get_button: return the latest button press from the button queue

        :return: string identifying the last button that was pressed
        """
        if key in self.button_queue_keys:
            queue_empty = GuiTab.ButtonQueues[key].empty()
        else:
            raise KeyError("GuiTab instance does not have access to button queue {}, or the specified queue has not"
                           "been created".format(key))

        if not queue_empty:
            button_ret = GuiTab.ButtonQueues[key].get(timeout=1)
        else:
            button_ret = False

        return button_ret

    def add_button_to_queues(self, button=None, button_text=None, queue_keys=None):
        """add_button_to_queues: Triggered when a QPushButton is clicked. Adds the button identifier to all queues that
                                 an instance has access to.
        """
        if button is not None:
            button_text = button.objectName()
        elif button_text is not None:
            pass
        else:
            raise ValueError("Must pass either a button or button text string argument!")

        button_str_split = button_text.split('_')
        button_queue_entry = {"Tab": button_str_split[0], "Get/Set": button_str_split[1],
                              "Instrument": button_str_split[2], "Parameter": button_str_split[3]}

        if queue_keys is None:
            for key in self.button_queue_keys:
                GuiTab.ButtonQueues[key].put(button_queue_entry)
        else:
            for key in queue_keys:
                GuiTab.ButtonQueues[key].put(button_queue_entry)

    def clear_button_queue(self, key):
        """clear_button_queue: clear the specified button queue of all values
        :return: None
        """
        if key in self.button_queue_keys:
            queue = GuiTab.ButtonQueues[key]
            while not queue.empty():
                queue.get(timeout=1)
        else:
            raise KeyError("GuiTab instance does not have access to button queue {}, or the specified queue has not"
                           "been created".format(key))

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

    def get_parameters(self, params, arg=None):
        """get_params: return the specified parameters as a dictionary.

        :param:
            params: string, list of strings, or "All" to specify which parameters
                    should be returned.

            arg: some getters take an additional argument. This keyword argument will be passed to the getter
                 if its value is changed from NoneType
        :return: dictionary of the desired parameters.
        """
        return_dict = {}
        method_list = []
        if params == 'all':
            for p in self.parameters:
                method_list.append((p, self.get_methods[p]))
        elif type(params) is list:
            for p in params:
                method_list.append((p, self.get_methods[p]))
        elif type(params) is str:
            method_list.append((params, self.get_methods[params]))

        for method in method_list:
            if arg is not None:
                return_dict[method[0]] = method[1](arg)
            else:
                return_dict[method[0]] = method[1]()

        return return_dict

    def set_parameters(self, params_dict):
        """set_params: set the specified parameters in the dialog display.

        :param params_dict: dictionary with keys and values of parameters to update
        :return: None
        """
        for key in params_dict:
            try:
                self.set_methods[key](params_dict[key])
            except KeyError as e:
                pass

    # Stacked widget switching #
    def _on_stacked_widget_select(self):
        """_on_stacked_widget_select: Change the stacked widget window according to the combo box window selector
        """
        cur_window = self.child.form.currentWidget().windowTitle()
        new_index = self.window_selector_dict[cur_window].currentIndex()
        self.child.form.setCurrentIndex(new_index)
        new_window = self.child.form.currentWidget().windowTitle()
        self.window_selector_dict[new_window].setCurrentIndex(new_index)

    def get_widgets_from_layout(self, layout):
        """get_widgets_from_layout: Recursively iterate through all layouts/tabs/stacks within a main widget and
                                    retrieve all sub widgets embedded within.

            Params: layout: layout, tab, or stacked widget object to iterate through
            Returns: flat list of all widgets
        """
        widget_list = []
        all_widgets = False
        while not all_widgets:
            # Get all widgets from the passed layout or tab/stacked widget #################################
            layout_type = type(layout)
            if issubclass(layout_type, QtWidgets.QLayout) or isinstance(layout, QtWidgets.QLayout):
                widgets = [layout.itemAt(i) for i in range(layout.count())]
            elif issubclass(layout_type, QtWidgets.QTabWidget) or isinstance(layout, QtWidgets.QTabWidget)\
                 or issubclass(layout_type, QtWidgets.QStackedWidget) or isinstance(layout, QtWidgets.QStackedWidget):
                widgets = [layout.widget(i) for i in range(layout.count())]
            else:
                widgets = None
            ################################################################################################

            # Iterate over all retrieved widgets #############################
            for w in widgets:
                w_type = type(w)
                if w_type is QtWidgets.QWidgetItem:
                    widget = w.widget()
                else:
                    widget = w
                widget_type = type(widget)

                if widget_type is QtWidgets.QWidget:
                    widget = widget.layout()
                    widget_type = type(widget)

                if issubclass(widget_type, QtWidgets.QLayout) or isinstance(widget, QtWidgets.QTabWidget):
                    widget_list.append(self.get_widgets_from_layout(widget))
                else:
                    widget_list.append(w)
            all_widgets = True
            ##################################################################

        # Return flattened widget list #############################################
        fwidget_list = flatten_list(widget_list)
        return fwidget_list
        ############################################################################
