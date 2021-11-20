""" This module implements the top-level classes and methods used in the focus calibration control software. Classes implemented include:

        :class:`.InstrumentSuite`: Top-level container class which holds all instruments in a given experiment. 

"""

class InstrumentSuite:
    """ The top-level container for all instruments in an experiment. The InstrumentSuite instance supports instrument loading
        by directly passing Instrument objects, or by providing a loaded json file object specifying the Instrument objects
        to instantiate. LINK TO INSTRUMENT SUITE EXAMPLE for an example of using this class.
    """

    def __init__(self, hw_cfg):
        """ 
        :param hw_cfg: (list) list containing Instrument objects and json file objects specfying the instruments in an experiment.         
        """
        pass

