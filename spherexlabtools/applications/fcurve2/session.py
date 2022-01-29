from .threads import ImageWriteThread, ImageDisplayThread, ProcedureThread


class FocusCurveSession:

    _image_write_thread = ImageWriteThread()
    _image_display_thread = ImageDisplayThread()
    _procedure_thread = ProcedureThread()

    def __init__(self):
        pass

    def start_image_write(self):
        """ Start the image write thread.
        """
        self._image_write_thread.start()

    def start_image_display(self):
        """ Start the image write thread.
        """
        self._image_display_thread.start()

    def start_procedure(self):
        """ Start the image write thread.
        """
        print("Display thread status %s" % str(self._image_display_thread.is_alive()))

    def stop_image_write(self):
        """ Start the image write thread.
        """
        self._image_write_thread.kill()
        self._image_write_thread.join()

    def stop_image_display(self):
        """ Start the image write thread.
        """
        self._image_display_thread.kill()
        self._image_display_thread.join()

    def stop_procedure(self):
        """ Start the image write thread.
        """
        pass














