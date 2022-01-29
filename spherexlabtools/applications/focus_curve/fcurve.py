""" This module provides a pymeasure procedure to run an automated focus curve measurement

Sam Condon, 01/05/2022
"""
import time
import logging
import numpy as np
from pymeasure.experiment import Procedure
from pymeasure.experiment import IntegerParameter, FloatParameter, Parameter


class FocusCurveProc(Procedure):

    # define procedure parameters
    focus_position = FloatParameter("Focus Position", units="step position", default=0)
    frames_per_image = IntegerParameter("Frames Per Image", default=10)
    images = IntegerParameter("Images", default=1)
    output_directory = Parameter("Output Directory", default=".")
    filename = Parameter("Filename", default="fcurveproc")

    mscope = None
    exp_source = None

    def __init__(self, mscope, exp_source, cfg, wait_event=None):
        """ Initialize a new procedure instance.

        :param: mscope: Microscope object to run procedure with.
        :param: exp_source: Any object with a "data" attribute where image data is retrieved.
        :param: configuration dictionary
        :param: wait_event: optional threading.Event object to wait on before reading image data.
        """
        self.mscope = mscope
        self.exp_source = exp_source
        for item in cfg:
            setattr(FocusCurveProc, item, cfg[item])
        self.wait_event = wait_event
        super().__init__()
        self.running = False

    def execute(self):
        # get parameters of the measurement #
        """
        frame_rate = self.mscope.cam_acquisition_frame_rate
        frame_width = self.mscope.cam_exposure_width
        frame_height = self.mscope.cam_exposure_height
        dtype = self.exp_source.data.dtype
        """

        logging.debug("Executing procedure {}".format(self))
        self.running = True

        try:
            # move focuser and wait for its motion to complete #
            self.mscope.focuser_step_position = self.focus_position
            self.mscope.focuser_wait_for_completion()

            # take a set of images that are averaged over several frames and write out to file. #
            for i in range(int(self.images)):

                # integrate image over specified number of exposures #
                image = np.zeros([2048, 2448], dtype=np.uint64)
                for e in range(int(self.frames_per_image)):
                    if self.wait_event is not None:
                        self.wait_event.wait()
                    exp = self.exp_source.data
                    if self.wait_event is not None:
                        self.wait_event.clear()
                    image = image + (exp / self.frames_per_image)
                    print(type(image), image.dtype)

                # write out integrated image to file #
                dtype = exp.dtype
                self.emit("results", {
                    "message": "gauge position = %s" % self.mscope.absolute_position,
                    "image": image.astype(dtype),
                    "image_path": self.output_directory,
                    "image_name": "%s.jpg" % self.filename
                    }
                )

        except Exception as e:
            print(e)

        logging.debug("Procedure {} complete.".format(self))
        self.running = False

