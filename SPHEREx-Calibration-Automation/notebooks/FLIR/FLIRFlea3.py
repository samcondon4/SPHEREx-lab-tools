import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import PySpin


class FLIRNode:

    def __init__(self, type_=None, node_=None, name_=None, val_=None):
        self.type = type_
        self.node = node_
        self.name = name_
        self.val = val_


class FLIRFlea3:

    def __init__(self):
        ##Analog Control nodes##############################
        self.analog_control = {
            'Gain': FLIRNode(name_='Gain', type_='float'),
            'GainAuto': FLIRNode(name_='GainAuto', type_='enum'),
            'BlackLevel': FLIRNode(name_='BlackLevel', type_='float'),
            'BlackLevelEnabled': FLIRNode(name_='BlackLevelEnabled', type_='bool'),
            'Gamma': FLIRNode(name_='Gamma', type_='float'),
            'GammaEnabled': FLIRNode(name_='GammaEnabled', type_='bool'),
            'Sharpness': FLIRNode(name_='Sharpness', type_='int'),
            'SharpnessEnabled': FLIRNode(name_='SharpnessEnabled', type_='bool'),
            'SharpnessAuto': FLIRNode(name_='SharpnessAuto', type_='enum'),
            'HueEnabled': FLIRNode(name_='HueEnabled', type_='bool'),
            'SaturationEnabled': FLIRNode(name_='SaturationEnabled', type_='bool')
        }
        ###################################################

        ##Image Format Control nodes#######################
        self.image_format_control = {
            'Width': FLIRNode(name_='Width', type_='int'),
            'Height': FLIRNode(name_='Height', type_='int'),
            'OffsetX': FLIRNode(name_='OffsetX', type_='int'),
            'OffsetY': FLIRNode(name_='OffsetY', type_='int'),
            'ReverseX': FLIRNode(name_='ReverseX', type_='bool'),
            'PixelFormat': FLIRNode(name_='PixelFormat', type_='enum'),
            'VideoMode': FLIRNode(name_='VideoMode', type_='enum'),
            'pgrPixelBigEndian': FLIRNode(name_='pgrPixelBigEndian', type_='bool'),
            'BinningHorizontal': FLIRNode(name_='BinningHorizontal', type_='int'),
            'BinningVertical': FLIRNode(name_='BinningVertical', type_='int'),
            'PixelDynamicRangeMin': FLIRNode(name_='PixelDynamicRangeMin', type_='int'),
            'PixelDynamicRangeMax': FLIRNode(name_='PixelDynamicRangeMax', type_='int')
        }
        ####################################################

        ##Acquisition Control nodes#########################
        self.acquisition_control = {
            'AcquisitionMode': FLIRNode(name_='AcquisitionMode', type_='enum'),
            'AcquisitionStart': FLIRNode(name_='AcquisitionStart', type_='cmd'),
            'AcquisitionStop': FLIRNode(name_='AcquisitionStop', type_='cmd'),
            'AcquisitionFrameCount': FLIRNode(name_='AcquisitionFrameCount', type_='int'),
            'AcquisitionFrameRate': FLIRNode(name_='AcquisitionFrameRate', type_='float'),
            'AcquisitionFrameRateEnabled': FLIRNode(name_='AcquisitionFrameRateEnabled', type_='bool'),
            'AcquisitionFrameRateAuto': FLIRNode(name_='AcquisitionFrameRateAuto', type_='enum'),
            'TriggerSelector': FLIRNode(name_='TriggerSelector', type_='enum'),
            'TriggerMode': FLIRNode(name_='TriggerMode', type_='enum'),
            'TriggerSource': FLIRNode(name_='TriggerSource', type_='enum'),
            'TriggerSoftware': FLIRNode(name_='TriggerSoftware', type_='cmd'),
            'TriggerActivation': FLIRNode(name_='TriggerActivation', type_='enum'),
            'TriggerDelay': FLIRNode(name_='TriggerDelay', type_='float'),
            'TriggerDelayEnabled': FLIRNode(name_='TriggerDelayEnabled', type_='bool'),
            'ExposureMode': FLIRNode(name_='ExposureMode', type_='enum'),
            'ExposureTime': FLIRNode(name_='ExposureTime', type_='float'),
            'ExposureAuto': FLIRNode(name_='ExposureAuto', type_='enum')
        }
        ####################################################

        ##Initialize FLIR system###############################################
        self.system = PySpin.System.GetInstance()
        # only one camera present in system so just grab first in list
        self.cam = self.system.GetCameras()[0]
        # grab transport layer device nodemap
        self.nodemap_tl_dev = self.cam.GetTLDeviceNodeMap()
        # grab transport layer stream nodemap
        self.nodemap_tl_stream = self.cam.GetTLStreamNodeMap()
        # initialize camera
        self.cam.Init()
        # grab GenICam nodemap
        self.nodemap_gen = self.cam.GetNodeMap()
        #######################################################################

        ##Initialize nodes in dictionaries##
        self.GetAnalogControl('all')
        self.GetImageFormatControl('all')
        self.GetAcquisitionControl('all')
        ####################################

    def BeginCapture(self):
        '''
        BeginCapture: Start image acquisition engine with current settings.
        '''
        self.cam.BeginAcquisition()

    def EndCapture(self):
        '''
        StopCapture: Stop image acquisition engine
        '''
        self.cam.EndAcquisition()

    def GetImage(self, timeout=1000):
        '''
        GetImage: Return numpy array with data for most recent camera image
        '''
        im = self.cam.GetNextImage(timeout)
        if im.IsIncomplete():
            print('Image incomplete with image status %d ...' % im.GetImageStatus())
            im_data = 0
        else:
            im_data = im.GetNDArray()
        return im_data

    def SetAnalogControl(self, node, val):
        '''
        SetAnalogControl: set node in analog control category.

            Params:
                node:   analog control parameter to set. Should be a key value to the self.AnalogControl
                        dictionary

            Returns:
                success_code: 0 indicates failure, 1 indicates successful set operation
        '''
        success_code = 1
        try:
            self.__set_node(self.analog_control[node], val)
        except TypeError as e:
            success_code = 0
            print(e)

    def SetImageFormatControl(self, node, val):
        '''
        SetImageFormatControl: set node in image format control category.

            Params:
                node:   image format control node to set. Should be a key value to the self.ImageFormatControl
                        dictionary.

            Returns:
                success_code: 0 indicates failure, 1 indicates successful set operation
        '''
        success_code = 1
        try:
            self.__set_node(self.image_format_control[node], val)
        except TypeError as e:
            success_code = 0
            print(e)

    def SetAcquisitionControl(self, node, val):
        '''
        SetAcquisitionControl: set node in the acquisition control category.

            Params:
                node:   acquisition control node to set. Should be a key value to the self.AcquisitionControl
                        dictionary.

                val: value to set on specified node.

            Returns:
                success_code: 0 indicates failure, 1 indicates successful set operation
        '''
        success_code = 1
        try:
            self.__set_node(self.acquisition_control[node], val)
        except TypeError as e:
            success_code = 0
            print(e)

        return success_code

    def GetAnalogControl(self, node):
        '''
        GetAnalogControl: get node in the analog control category. Updates node stored in self.AnalogControl
        and returns its associated value.

            Params:
                node:   analog control node to get. Should be a key value to the self.AnalogControl dictionary
                        or 'all' to specify that all nodes in self.AnalogControl should be updated.
        '''
        if node == 'all':
            ret_node = []
            for key in self.analog_control:
                ret_node.append(self.__get_node(self.analog_control[key], self.nodemap_gen))
        else:
            key = node
            ret_node = self.__get_node(self.analog_control[key], self.nodemap_gen)

        return self.analog_control[key]

    def GetImageFormatControl(self, node):
        '''
        GetImageFormatControl: get node in the image format control category.

            Params:
                node:   image format control node to get. Should be a key value to the self.ImageFormatControl
                        dictionary or 'all' to specify that all nodes in self.ImageFormatControl should be updated.
        '''
        if node == 'all':
            ret_node = []
            for key in self.image_format_control:
                ret_node.append(self.__get_node(self.image_format_control[key], self.nodemap_gen))
        else:
            key = node
            ret_node = self.__get_node(self.image_format_control[key], self.nodemap_gen)

        return self.image_format_control[key]

    def GetAcquisitionControl(self, node):
        '''GetAcquisitionControl: get node in the acquisition control category.

        Params:
            node:   image format control node to get. Should be a key value to the self.AcquisitionControl
                    dictionary or 'all' to specify that all nodes in self.ImageFormatControl should be updated.
        '''
        if node == 'all':
            ret_node = []
            for key in self.acquisition_control:
                ret_node.append(self.__get_node(self.acquisition_control[key], self.nodemap_gen))
        else:
            key = node
            ret_node = self.__get_node(self.acquisition_control[key], self.nodemap_gen)

        return self.acquisition_control[key]

    def PrintNodeValues(self):
        # self.GetAcquisitionControl('all')
        print('ANALOG CONTROL NODES: \n')
        for key in self.analog_control:
            print('{}: {}'.format(key, self.analog_control[key].val))

        print('\n\nIMAGE FORMAT CONTROL NODES: \n')
        for key in self.image_format_control:
            print('{}: {}'.format(key, self.image_format_control[key].val))

        print('\n\nACQUISITION CONTROL NODES: \n')
        for key in self.acquisition_control:
            print('{}: {}'.format(key, self.acquisition_control[key].val))

    def __set_node(self, flirnode, val):
        '''__set_node:  private helper function used in all public setter functions.
                        Sets value of specified node in the FLIR nodemap.

        '''
        node_valid = 1
        if PySpin.IsWritable(flirnode.node):
            if flirnode.type == 'enum':
                nodeset = flirnode.node.GetEntryByName(val)
                if not PySpin.IsAvailable(nodeset) or not PySpin.IsReadable(nodeset):
                    print('Unable to set node {} to {}'.format(flirnode.name, val))
                    node_valid = 0
                else:
                    flirnode.node.SetIntValue(nodeset.GetValue())

            elif flirnode.type == 'cmd':
                flirnode.node.Execute()

            elif flirnode.type == 'float':
                if type(val) == float:
                    flirnode.node.SetValue(val)
                elif type(val) == int:
                    flirnode.node.SetValue(float(val))
                else:
                    node_valid = 0
                    raise TypeError('This node expects a float and a {} was given'.format(type(val)))

            elif flirnode.type == 'bool':
                if type(val) == bool:
                    flirnode.node.SetValue(val)
                else:
                    node_valid = 0
                    raise TypeError('This node expects a boolean and a {} was given'.format(type(val)))

            elif flirnode.type == 'int':
                if type(val) == int:
                    flirnode.node.SetValue(val)
                else:
                    node_valid = 0
                    raise TypeError('This node expects an integer and a {} was given'.format(type(val)))

            else:
                node_valid = 0
                print('Flirnode type has not been set to valid type. No action taken.')
        else:
            node_valid = 0
            raise RuntimeError('Node "{}" is not writeable'.format(flirnode.name))

        if node_valid:
            # update flirnode instance
            return self.__get_node(flirnode, flirnode.node.GetNodeMap())
        else:
            return 0

    def __get_node(self, flirnode, nodemap):
        '''__get_node:  private helper function used in all public getter functions.
                        Updates the passed FLIRNode object with most recent data as
                        read from camera.

        '''
        node = nodemap.GetNode(flirnode.name)
        node_valid = 1
        val = None
        if flirnode.type == 'enum':
            node = PySpin.CEnumerationPtr(node)
            if PySpin.IsReadable(node):
                val = node.GetCurrentEntry().GetSymbolic()

        elif flirnode.type == 'cmd':
            node = PySpin.CCommandPtr(node)

        elif flirnode.type == 'float':
            node = PySpin.CFloatPtr(node)
            if PySpin.IsReadable(node):
                val = node.GetValue()

        elif flirnode.type == 'bool':
            node = PySpin.CBooleanPtr(node)
            if PySpin.IsReadable(node):
                val = node.GetValue()

        elif flirnode.type == 'int':
            node = PySpin.CIntegerPtr(node)
            if PySpin.IsReadable(node):
                val = node.GetValue()

        elif flirnode.type == 'str':
            node = PySpin.CStringPtr(node)

        else:
            node_valid = 0
            print('No valid node type has been set on %s' % name)

        if node_valid:
            flirnode.node = node
            flirnode.val = val
        else:
            ret_node = 0
