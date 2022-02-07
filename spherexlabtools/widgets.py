""" Module implementing a set of Qt widgets used in the controllers.

Sam Condon, 02/06/2022
"""

import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree


class SequenceGroup(pTypes.GroupParameter):
    """ Expandable GroupParameter implementing the sequence tree.
    """
    def __init__(self, params, **opts):
        opts["name"] = "Sequence"
        opts["type"] = "group"
        opts["addText"] = "Add"
        opts["addList"] = [p["name"] for p in params]
        self.level = Parameter.create(name="Level", type="str", value="x")
        self.remove = Parameter.create(name="Remove", type="action")
        self.base_children = [self.level, self.remove]
        opts["children"] = self.base_children
        pTypes.GroupParameter.__init__(self, **opts)

        # connect buttons to methods #
        self.remove.sigStateChanged.connect(self.remove_child)

    def addNew(self, typ=None):
        """ Add a child to the sequence tree.
        """
        level = self.level.value().split(".")
        children = self.children()
        child = self
        insert_pos = len(children) - len(self.base_children)
        insert_level = len(children) - len(self.base_children)
        for lvl in level:
            if lvl == "x":
                child.insertChild(insert_pos, dict(name=str(insert_level) + ": " + typ, type="str", value="",
                                                   removeable=True))
            else:
                child = children[int(lvl)]
                children = child.children()
                insert_pos = len(children)
                insert_level = len(children)

    def remove_child(self):
        """ Remove a child at the specified level from the sequence tree.
        """

        level = self.level.value().split(".")
        children = self.children()
        child = self
        for lvl in level:
            child = children[int(lvl)]
            children = child.children()

        # get the current child parent #
        parent = child.parent()

        # remove specified child #
        if child not in self.base_children:
            parent.removeChild(child)

        # rename children #
        children = parent.children()
        for i in range(len(children)):
            child = children[i]
            if child not in self.base_children:
                name = child.name().split(":")[-1].strip()
                child.setName(str(i) + ": " + name)


class Sequencer(pTypes.GroupParameter):
    """ GroupParameter type wrapping the :class:`.SequenceGroup`
    """

    def __init__(self, params, **opts):
        """ Initialize the sequencer.

        :param: params: Parameters to sequence through.
        """
        opts["name"] = "Procedure Sequencer"
        opts["type"] = "group"
        self.sequence_group = SequenceGroup(params)
        self.start_sequence = Parameter.create(name="Start Procedure Sequence", type="action")
        self.pause_sequence = Parameter.create(name="Pause Procedure Sequence", type="action")
        self.stop_sequence = Parameter.create(name="Abort Procedure Sequence", type="action")
        self.base_children = [self.sequence_group, self.start_sequence, self.pause_sequence, self.stop_sequence]
        opts["children"] = self.base_children
        pTypes.GroupParameter.__init__(self, **opts)

        # connect buttons to methods #
        self.start_sequence.sigStateChanged.connect(self.get_sequence)

    def get_sequence(self):
        """ Method to retrieve all of the sequence parameters.
        """
        print(self.sequence_group.getValues())
