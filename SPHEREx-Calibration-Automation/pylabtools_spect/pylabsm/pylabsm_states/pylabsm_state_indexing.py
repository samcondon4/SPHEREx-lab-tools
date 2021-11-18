"""pylabsm_state_indexing:

    This module implements the indexing state class.

"""

from pylabsm.pylabsm_states.pylabsm_basestate import SmCustomState


class Indexing(SmCustomState):

    def __init__(self, sm, identifier="indexing", **kwargs):
        super().__init__(sm, self, identifier, **kwargs)
        self.sequence = None
        self.series = None

    def indexing_action(self, in_dict):

        # By the time the indexing state is reached, all the other states will have generated their state specific
        # control loop. So clear the "Control Loop Generate" flag.
        in_dict["Control Loop Generate"][0] = False
        ser_index = in_dict["Series Index"]
        seq_index = in_dict["Sequence Index"]
        print("## INDEX VALUES: series = {}, sequence = {}".format(ser_index[0], seq_index[0]))
        in_dict["Control Loop Complete"][0] = False
        mdk_list = list(in_dict["Moving"].keys())
        # update the current sequence/series if necessary ######################
        if self.sequence is None:
            self.sequence = in_dict["Moving"][mdk_list[0]][ser_index[0]]
        if self.series is None:
            self.series = in_dict["Moving"][mdk_list[0]]

        # perform indexing using the lengths of the sequences/series ############
        if seq_index[0] < len(self.sequence) - 1:
            seq_index[0] += 1
        elif ser_index[0] < len(self.series) - 1:
            self.sequence = None
            ser_index[0] += 1
            seq_index[0] = 0
        else:
            ser_index[0] = 0
            seq_index[0] = 0
            self.sequence = None
            self.series = None
            in_dict["Control Loop Complete"][0] = True
