"""gui_window:

    This module provides a set of base classes for PyQt windows allowing PyQt interactive GUIs to be constructed
    in a streamlined manner.

Sam Condon, 08/12/2021
"""

import asyncio
import numpy as np
from PyQt5 import QtCore, QtWidgets
from pylabgui.pylabgui_widget_group import WidgetGroup, ListWidgetGroup


# Miscellaneous helper functions ################################################################
def flatten_list(in_list):
    flist = []
    [flist.extend(flatten_list(e)) if type(e) is list else flist.extend([e]) for e in in_list]
    return flist
#################################################################################################


class GuiWindow:
    WidgetGroups = {}

    @classmethod
    def get_widgets_from_layout(cls, layout):
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
            elif issubclass(layout_type, QtWidgets.QTabWidget) or isinstance(layout, QtWidgets.QTabWidget) \
                    or issubclass(layout_type, QtWidgets.QStackedWidget) or isinstance(layout,
                                                                                       QtWidgets.QStackedWidget):
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
                    widget_list.append(cls.get_widgets_from_layout(widget))
                else:
                    widget_list.append(w)
            all_widgets = True
            ##################################################################

        # Return flattened widget list #############################################
        fwidget_list = flatten_list(widget_list)
        return fwidget_list
        ############################################################################

    @classmethod
    def get_widget_dict(cls, widget):
        """get_widget_dict: This method takes as input a qwidget and returns a dictionary containing its identification
                            for automatic gui configuration. Widgets passed into this method must have been named
                            according to the following naming convention:

                            <widget type>_<group type>_<widget group>_<widget action>_<widget name>

                            Within each <>, if multiple words are to be used, the words should be spelled in camel-case.

        :return: widget_dict = {"type": <widget type string>, "group_type": <type of group the widget belongs to>,
                                "widget_group": <widget group identifier>, "widget_action": <type of action associated
                                with this widget (get/set parameters or passive)>}
        """

        # Create empty return dictionary.
        widget_dict = {"Type": None, "GroupTypes": None, "Groups": None, "Actions": None, "Name": None}
        # Widget dictionary keys that may need multiple string splits.
        sub_split_keys = ["GroupTypes", "Groups", "Actions"]
        upper_split_keys = sub_split_keys + ["Name"]
        wdict_keys = list(widget_dict.keys())
        widget_str_split = widget.objectName().split("_")
        try:
            for k in range(len(wdict_keys)):
                wkey = wdict_keys[k]
                if wkey in sub_split_keys:
                    widget_dict[wkey] = widget_str_split[k].split("X")
                elif wkey in upper_split_keys:
                    widget_dict[wkey] = [widget_str_split[k]]
                else:
                    widget_dict[wkey] = widget_str_split[k]
            for key in upper_split_keys:
                sub_split_list = widget_dict[key]
                for k in range(len(sub_split_list)):
                    string = sub_split_list[k]
                    upper_inds = np.where(np.array([1 if string[k].isupper() else 0 for k in range(len(string))]) == 1)[0]
                    if len(upper_inds) > 0:
                        new_str = ""
                        for i in range(len(upper_inds) - 1):
                            new_str += string[upper_inds[i]: upper_inds[i+1]].lower() + " "
                        new_str += string[upper_inds[-1]:].lower()
                    else:
                        new_str = string
                    widget_dict[key][k] = new_str

            widget_dict["Name"] = widget_dict["Name"][0]

        except IndexError as e:
            widget_dict = False

        if widget_dict is not False:
            widget_dict["Widget"] = widget

        return widget_dict

    def __init__(self, child=None, form=None, data_queues=None):
        self.child = child
        self.data_queues = data_queues
        if form is None:
            self.form = QtWidgets.QDialog()
        else:
            self.form = form
        self.widget_list = None
        self.configured = False

    def configure(self):
        """configure: configure widgets inside of a layout into widget groups according to the widget name specification.
        """
        self.widget_list = [w.widget() for w in GuiWindow.get_widgets_from_layout(self.form.layout())
                            if w.widget() is not None]
        widget_dicts = [GuiWindow.get_widget_dict(widget) for widget in self.widget_list]
        # Place widgets into appropriate groups ###############################################################
        for widget in self.widget_list:
            widget_dict = GuiWindow.get_widget_dict(widget)
            if widget_dict is not False:
                wtype = widget_dict["Type"]
                groups = widget_dict["Groups"]
                group_types = widget_dict["GroupTypes"]
                actions = widget_dict["Actions"]
                for i in range(len(groups)):
                    igroup = groups[i]
                    igtype = group_types[i]
                    iaction = actions[i].replace(" ", "_")
                    if igroup not in GuiWindow.WidgetGroups:
                        GuiWindow.WidgetGroups[igroup] = WidgetGroup(igroup, data_queues=self.data_queues) \
                                                         if igtype == "base" else \
                                                         ListWidgetGroup(igroup, data_queues=self.data_queues)
                    getattr(GuiWindow.WidgetGroups[igroup], "add_{}".format(iaction))(widget_dict)
        ##########################################################################################################

        # Configure widget groups ####################################################
        for group in GuiWindow.WidgetGroups:
            wgroup = GuiWindow.WidgetGroups[group]
            if not wgroup.is_configured():
                wgroup.configure()
        ##############################################################################

        self.configured = True

    def get(self, group, get_list):
        """get: Calls all getter methods specified by get_list in the WidgetGroup specified by group. Return the getter
                method return values in a dictionary.

        :param group: WidgetGroup to run getter methods of
        :param get_list: list of getters within group to run
        :return: Dictionary of the form {group: {getter: getter return value}}
        """
        widget_group = self.WidgetGroups[group]
        if widget_group.configured:
            params_dict = widget_group.get_passive(get_list)
        else:
            raise RuntimeError("Group {} has not been configured yet!".format(group))

        return {group: params_dict}

    def set(self, group, set_dict):
        """set: Calls all setter methods specified by the keys of set_dict in the WidgetGroup specified by group.

        :param group: WidgetGroup to run setter methods of
        :param set_dict: Dictionary with keys corresponding to the setter method and values corresponding to the setter
                         arguments to pass to the setter method.
        :return: None
        """
        widget_group = self.WidgetGroups[group]
        """
        if widget_group.configure:
            widget_group.set_passive(set_dict)
        else:
            raise RuntimeError("Group {} has not been configured yet!".format(group))
        """


class GuiCompositeWindow(GuiWindow):

    def __init__(self, child=None, window_type=None):
        self.child = child
        if window_type == "stacked":
            form = QtWidgets.QStackedWidget()
        elif window_type == "tab":
            form = QtWidgets.QTabWidget()
        else:
            form = None
        self.stacked_selector_dict = None
        super().__init__(child=self.child, form=form)

    def add_widget(self, widget):
        """add_widget: add a widget to the form attribute according to the widget type of self.form
        :return: None
        """
        form_type = type(self.form)
        if form_type == QtWidgets.QStackedWidget:
            self.form.addWidget(widget)
        elif form_type == QtWidgets.QTabWidget:
            self.form.addTab(widget, widget.windowTitle())

    def configure(self):
        """configure: Override the GuiWindow class configure method to configure a composite widget window.
        """
        form_type = type(self.form)
        if form_type is QtWidgets.QStackedWidget:
            self.configure_stacked_widget_switch()

    def configure_stacked_widget_switch(self):
        """configure_stacked_widget_switch: Stacked widgets do not naturally provide any means of switching between
                                            the tabs that have been added. This method builds a dropdown menu to switch
                                            between the windows of a stacked widget.

        params: None
        return: None
        """
        widget_list = [self.child.form.widget(i) for i in range(self.child.form.count())]
        self.stacked_selector_dict = {}
        for widget in widget_list:
            window_selector = QtWidgets.QComboBox()
            widget_name = widget.windowTitle()
            layout = widget.layout()

            for w in widget_list:
                window_selector.addItem(w.windowTitle())

            window_selector.currentIndexChanged.connect(self._on_stacked_widget_select)
            layout.addWidget(window_selector, 0, layout.columnCount() - 1)
            widget.setLayout(layout)
            self.stacked_selector_dict[widget_name] = window_selector

    def _on_stacked_widget_select(self):
        """_on_stacked_widget_select: Change the stacked widget window according to the combo box window selector
        """
        cur_window = self.child.form.currentWidget().windowTitle()
        new_index = self.stacked_selector_dict[cur_window].currentIndex()
        self.child.form.setCurrentIndex(new_index)
        new_window = self.child.form.currentWidget().windowTitle()
        self.stacked_selector_dict[new_window].setCurrentIndex(new_index)
