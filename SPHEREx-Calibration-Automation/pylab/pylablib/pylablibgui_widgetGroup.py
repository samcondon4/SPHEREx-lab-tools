"""widget_group:

    This module provides the classes to implement widget groups.

    Widget group actions:
        passive: user input widgets (line edit, combobox, checkbox, etc.).
        passive list single: passive list where only the currently selected item is returned by get methods
        passive list all: passive list where all items are returned by get methods
        getter: get values of passive entries or the currently selected list widget entry.
        getter of all: get all list widget entries.
        setter: set values of passive entries or a list widget.
        remover: remove the currently selected entry from a list widget.
        remover of all: remove all entries from a list widget.
        list: list widget
        item display: Subset of passive used in ListWidgetGroups. These passive entries are display as list entry text.

Sam Condon, 08/12/2021
"""

import asyncio
from PyQt5 import QtCore, QtWidgets
from pylablib.QListWigetSubclass import QListWidgetItemCustom


class WidgetGroup:

    # Widget helper functions ################################################################
    # List operation methods ######################################
    @classmethod
    def add_item_to_list(cls, lst, item_dict):
        """add_item_to_list: add an item to the given list

        :param lst: QListWidget object to add an item to.
        :param item_dict: Dictionary containing item data and text to add to the QListWidget object. Dictionary is of
                          the form: {"text": <list item text>, "data": <list item data>}
        """
        list_item = QListWidgetItemCustom()
        list_item.setData(0, 0)
        list_item.setText(item_dict["text"])
        list_item.user_data = item_dict["data"]
        lst.addItem(list_item)

    @classmethod
    def add_items_to_list(cls, lst, item_dict_list):
        """Description: Add multiple items to the given list

        :param lst: QListWidget object to add items to.
        :param item_dict_list: List of dictionaries containing item data and text to add to the QListWidget object.
                               Dictionaries are of the form: {"text": <list item text>, "data": <list item data>}
        """
        for item_dict in item_dict_list:
            cls.add_item_to_list(lst, item_dict)

    @classmethod
    def set_items_to_list(cls, lst, item_dict_list):
        """Description: Same as add_items_to_list, but the list is cleared before the items are added.
        """
        lst.clear()
        cls.add_items_to_list(lst, item_dict_list)

    @classmethod
    def set_list_item_from_text(cls, lst, item_text):
        """Description: Set the currently selected list item to the list item with the given text
        """
        item = lst.findItems(item_text, QtCore.Qt.MatchExactly)[0]
        lst.setCurrentItem(item)

    @classmethod
    def get_item_from_list(cls, lst, textordata="data"):
        """get_item_from_list: Return the data from the currently selected item from the list.
        """
        get_item = lst.currentItem()
        if get_item is not None:
            if textordata == "data":
                ret_item = get_item.user_data
            elif textordata == "text":
                ret_item = get_item.text()
            else:
                raise RuntimeError("Only text or data can be returned from a QListWidgetItem")
        else:
            ret_item = False
        return ret_item

    @classmethod
    def get_all_items_from_list(cls, lst, textordata="data"):
        """get_all_items_from_list: Return all data from the list.
        """
        item_count = lst.count()
        item_data = [0 for _ in range(item_count)]
        for i in range(item_count):
            if textordata == "data":
                item_data[i] = lst.item(i).user_data
            elif textordata == "text":
                item_data[i] = lst.item(i).text()
        return item_data

    @classmethod
    def remove_item_from_list(cls, lst):
        """remove_item_from_list: Remove the currently selected item from the list without returning.
        """
        rem_item = lst.currentItem()
        if rem_item is not None:
            rem_row = lst.currentRow()
            lst.takeItem(rem_row)

    @classmethod
    def remove_all_items_from_list(cls, lst):
        lst.clear()

    #########################################################################################

    # Checkbox operation methods ##############################################
    @classmethod
    def set_check_state(cls, check_state, in_widget):
        if check_state == "False":
            in_widget.setCheckState(QtCore.Qt.Unchecked)
        else:
            in_widget.setCheckState(QtCore.Qt.Checked)
    ###########################################################################

    ############################################################################

    def __init__(self, group_name, child=None, data_queues=None):
        self.group_name = group_name
        self.child = child
        if data_queues is None:
            data_queues = []
        self.data_queues = data_queues
        self.getter = None
        self.setter = None
        self.get_methods = {}
        self.set_methods = {}
        self.getter_proc = None
        self.setter_proc = None
        self.passive = []
        self.configured = False

    def add_getter(self, widget_dict):
        """add_getter: Add a widget which when pressed will result in retrieval of all data stored in passive widgets.
        """
        getter_widget = widget_dict["Widget"]
        self.getter = getter_widget
        self.configured = False

    def set_getter_proc(self, getter_proc):
        """Description: Set the getter process method.

        :param getter_proc: Function object to process passive entries before returning.
        :return: None
        """
        self.getter_proc = getter_proc

    def add_setter(self, widget_dict):
        """add_setter: Add a widget which when pressed will result in assignment to the values of all passive widgets.
        """
        setter_widget = widget_dict["Widget"]
        self.setter = setter_widget
        self.configured = False

    def set_setter_proc(self, setter_proc):
        """Description: Set the setter process method.

        :param setter_proc: Function object to process setter data before calling setters.
        :return: None
        """
        self.setter_proc = setter_proc

    def add_passive(self, widget_dict):
        """add_passive: Add a passive widget element
        """
        self.passive.append(widget_dict)
        self.configured = False

    def add_passive_list_all(self, widget_dict):
        """add_passive_list_all: Add a passive list all widget element to the list of passive widgets.
        """
        self.passive.append(widget_dict)
        self.configured = False

    def is_configured(self):
        """is_configured: Returns true if the widget group with all of its current widgets have been configured to
                          communicate.
        """
        return self.configured

    def configure(self):
        self.configure_passive()
        if self.getter is not None:
            self.getter.clicked.connect(lambda state, add_to_queue=True: self.get_passive(add_to_queue=add_to_queue))

        self.configured = True

    def configure_passive(self):
        """configure_passive: Configure getter methods for passive widgets in a WidgetGroup.
        """
        # Iterate over all widgets in the list of passive widgets #####################################################
        for widge_dict in self.passive:
            widget = widge_dict["Widget"]
            wname = widge_dict["Name"]
            wactions = widge_dict["Actions"]
            wtype = type(widget)

            # Assign getter or setter method based on the type of the passive widget ############################
            if wtype is QtWidgets.QLineEdit:
                get_method = widget.text
                set_method = widget.setText

            elif wtype is QtWidgets.QComboBox:
                get_method = widget.currentText
                set_method = widget.setCurrentText

            elif wtype is QtWidgets.QCheckBox:
                get_method = lambda in_widget=widget: str(in_widget.checkState() > 0)
                set_method = lambda check_state, in_widget=widget: self.set_check_state(check_state, in_widget=in_widget)

            elif wtype is QtWidgets.QListWidget and "passive list all" not in wactions:
                get_method = lambda in_widget=widget, textordata="data": \
                                    WidgetGroup.get_item_from_list(in_widget, textordata=textordata)
                set_method = lambda item_dict=None, in_widget=widget: \
                                    WidgetGroup.set_list_item_from_text(in_widget, item_text=item_dict)

            elif wtype is QtWidgets.QListWidget and "passive list all" in wactions:
                get_method = lambda in_widget=widget, textordata="data": \
                    WidgetGroup.get_all_items_from_list(in_widget, textordata=textordata)
                set_method = lambda item_dict_list, in_widget=widget: \
                                    WidgetGroup.set_items_to_list(in_widget, item_dict_list=item_dict_list)

            else:
                get_method = None
                set_method = None
            ####################################################################################################

            # Add getter/setter to the get/set_method dictionary #####
            if get_method is not None:
                self.get_methods[wname] = get_method
            if set_method is not None:
                self.set_methods[wname] = set_method
            ##########################################################
            ###########################################################################################################

    def get_passive(self, get_list="All", add_to_queue=False):
        """get_passive: get all passive widget inputs and add their data to all instance data queues.
        """
        if get_list == "All":
            key_list = list(self.get_methods.keys())
        else:
            key_list = get_list
        passive_params = dict([(key, self.get_methods[key]()) for key in key_list])
        # Pass the returned parameters through the getter process function if one is present #######
        if self.getter_proc is not None:
            passive_params = self.getter_proc(passive_params)
        ############################################################################################

        # Update data queues #######################################################################
        if add_to_queue:
            for queue in self.data_queues:
                if type(queue) is asyncio.Queue:
                    queue.put_nowait({self.group_name: passive_params})
                else:
                    queue.put({self.group_name: passive_params})
        ############################################################################################

        return passive_params

    def set_passive(self, setter_dict):
        """set_passive: set all passive widget values
        :param: setter_dict: dictionary containing key/value pairs corresponding to how passive widget values should
                             be set.
        :return: None
        """
        # Run the setter dictionary through the process method if one exists.
        if self.setter_proc is not None:
            text, setter_dict = self.setter_proc(setter_dict)
        # Run setter methods according to key value pairs in setter_dict
        for key in setter_dict:
            if key in list(self.set_methods.keys()):
                self.set_methods[key](setter_dict[key])
            else:
                raise RuntimeError("Key {} not found in self methods for group {}".format(key, self.group_name))


class ListWidgetGroup(WidgetGroup):

    def __init__(self, group, data_queues=None):
        super().__init__(group, child=self, data_queues=data_queues)
        self.item_list = None
        self.item_display = []
        self.item_selector = None
        self.getter_of_all = None
        self.remover = None
        self.remover_of_all = None
        self.list_setter_proc = None

    def add_list(self, widget_dict):
        self.item_list = widget_dict["Widget"]
        self.configured = False
        self.item_selector = False

    def add_item_selector_list(self, widget_dict):
        self.item_list = widget_dict["Widget"]
        self.configured = False
        self.item_selector = True

    def add_remover(self, widget_dict):
        self.remover = widget_dict["Widget"]
        self.configured = False

    def add_remover_of_all(self, widget_dict):
        self.remover_of_all = widget_dict["Widget"]
        self.configured = False

    def add_item_display(self, widget_dict):
        self.add_passive(widget_dict)
        self.item_display.append(widget_dict["Name"])
        self.configured = False

    def get_item_display(self):
        """get_item_display: return the value of the current item display attribute
        """
        return self.item_display

    def set_list_setter_proc(self, setter_proc):
        """Description: Set the list setter process method. I.e. the method that will be called on passive data before
                        writing it to the list
        :param setter_proc: Setter process function object.
        :return: None
        """
        self.list_setter_proc = setter_proc

    def set_list_item(self, state=None, external=None):
        # If external list data has not been passed, then retrieve list data from passive entries ###
        if external is None:
            passive_data = self.get_passive(add_to_queue=False)
        else:
            passive_data = external
        #############################################################################################

        # If a setter process method has been set, then call it with the list data otherwise extract #
        # list item display text from the data #######################################################
        if self.list_setter_proc is not None:
            text, data = self.list_setter_proc(passive_data)
        else:
            display_keys = self.item_display
            entry_str = ""
            for i in range(len(display_keys) - 1):
                entry = display_keys[i]
                data = passive_data[entry]
                entry_str += "{}: {}, ".format(entry, data)
            entry = display_keys[-1]
            data = passive_data[entry]
            data = data.replace(": ", "")
            data = data.replace(";", "")
            entry_str += "{}: {};".format(entry, data)
            data, text = (passive_data, entry_str)
        ################################################################################################

        # Add the newly created list item to the list widget ###########################################
        WidgetGroup.add_item_to_list(self.item_list, {"text": text, "data": data})
        ################################################################################################

    def item_select(self):
        """item_select: This method retrieves the currently selected list item (when the currently selected item
                        changes) and displays the data contained in the item to the passive widgets.
        :return: None
        """
        cur_data = self.item_list.currentItem().user_data
        self.set_passive(cur_data)

    def remove_item(self):
        """Description: remove the currently selected item from the list
        :return:
        """
        if self.item_selector:
            self.item_list.currentItemChanged.disconnect()
            WidgetGroup.remove_item_from_list(self.item_list)
            self.item_list.currentItemChanged.connect(self.item_select)
        else:
            WidgetGroup.remove_item_from_list(self.item_list)

    def remove_all_items(self):
        """Description: remove all items from the list.
        :return:
        """
        if self.item_selector:
            self.item_list.currentItemChanged.disconnect()
            WidgetGroup.remove_all_items_from_list(self.item_list)
            self.item_list.currentItemChanged.connect(self.item_select)
        else:
            WidgetGroup.remove_all_items_from_list(self.item_list)

    def get_list(self):
        """Description: Get items from the item list
        :return: list item widgets
        """
        items = WidgetGroup.get_all_items_from_list(self.item_list, textordata="data")
        for queue in self.data_queues:
            queue.put_nowait(items)

    def configure(self):
        """configure: Configure list widget window.
        """
        if not self.configured:
            if self.setter is not None and "_configure" not in self.setter.objectName():
                self.setter.clicked.connect(self.set_list_item)
                setter_name = self.setter.objectName() + "_configured"
                self.setter.setObjectName(setter_name)

            if self.getter is not None and "_configure" not in self.getter.objectName():
                self.getter.clicked.connect(self.get_list)
                getter_name = self.getter.objectName() + "_configured"
                self.getter.setObjectName(getter_name)

            if self.remover is not None:
                self.remover.clicked.connect(self.remove_item)

            if self.remover_of_all is not None:
                self.remover_of_all.clicked.connect(self.remove_all_items)

            self.configure_passive()
            if self.item_list is not None and self.item_selector:
                self.item_list.setCurrentRow(0)
                self.item_list.currentItemChanged.connect(self.item_select)

        self.configured = True
