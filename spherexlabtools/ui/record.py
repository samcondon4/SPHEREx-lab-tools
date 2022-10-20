""" THis module implements the default interfaces for procedure Records.
"""
import os
from PyQt5 import QtCore
from pyqtgraph.parametertree import Parameter
import pyqtgraph.parametertree.parameterTypes as pTypes


class RecordUI(pTypes.GroupParameter):
    """ Group parameter type providing an interface to save and interact with :class:`.procedures.Record` classes.
    """

    new_record_params_sig = QtCore.pyqtSignal(object, object)
    save_record_sig = QtCore.pyqtSignal(object, object)

    save_record_name = "Save Single Record"

    def __init__(self, records, **opts):
        """ Initialize the interface.

        :param records: List of records to generate the interface around.
        """
        children = [None for _ in records]
        i = 0
        for rec in records.values():
            buffer_size = {"name": "Buffer Size", "type": "int", "value": 1}
            integrate_buffer = {"name": "Integrate Buffer", "type": "bool", "value": False}
            # TODO: Add ability to generate a true histogram #
            ancillary_gen = {"name": "Run Ancillary Generator", "type": "bool", "value": False}
            save_param = Parameter.create(name=self.save_record_name, type="action", children=[
                {"name": "File-path", "type": "str", "value": os.path.join(os.getcwd(), "Record")},
                {"name": "Type", "type": "list", "limits": [".pkl", ".mat"]}
            ])
            params = [buffer_size, integrate_buffer, ancillary_gen, save_param]
            # recorders/viewers #
            if rec.viewer is not None:
                viewer_param = Parameter.create(name="Viewer", type="str", value=rec.viewer, enabled=False)
                params.append(viewer_param)
            if rec.recorder is not None:
                rec_param = Parameter.create(name="Recorder", type="str", value=rec.recorder, enabled=False)
                recorder_filepath = {"name": "Recorder Write Path", "type": "str", "value": os.path.join(os.getcwd(),
                                                                                                         rec.name)}
                params.extend([rec_param, recorder_filepath])
            children[i] = Parameter.create(name=rec.name, type="group", children=params)
            i += 1

        opts["children"] = children
        opts["name"] = "Records"
        opts["type"] = "group"
        pTypes.GroupParameter.__init__(self, **opts)
        for rec_param in children:
            rec_param_name = rec_param.name()
            for c in rec_param.children():
                if c.name() != self.save_record_name:
                    c.sigTreeStateChanged.connect(lambda param, changes, name=rec_param_name:
                                                  self.new_record_params_sig.emit(param, name))
                else:
                    c.sigActivated.connect(lambda param, name=rec_param_name: self.save_record_sig.emit(param, name))
