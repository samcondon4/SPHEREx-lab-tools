""" Module implementing a set of Qt widgets used in the controllers.

Sam Condon, 02/06/2022
"""

import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree


class Sequencer(pTypes.GroupParameter):
    """ GroupParameter type implementing a tree for sequencing through a set of procedure parameters.
    """

    def __init__(self, params, **opts):
        """ Initialize the sequencer.

        :param: params: Parameters to sequence through.
        """
        opts["name"] = "Procedure Sequence"
        opts["type"] = "group"
        opts["addText"] = "Add"
        opts["addList"] = [p["name"] for p in params]
        self.level = Parameter.create(name="Level", type="str", value="x")
        self.remove = Parameter.create(name="Remove", type="action")
        self.base_children = [self.level, self.remove]
        opts["children"] = self.base_children
        pTypes.GroupParameter.__init__(self, **opts)

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

        # remove specified child #
        child.parent().removeChild(child)

        # rename children #
        for i in range(len(children)):
            child = children[i]
            name = child.name().split(":")[-1].strip()
            child.setName(str(i) + ": " + name)
