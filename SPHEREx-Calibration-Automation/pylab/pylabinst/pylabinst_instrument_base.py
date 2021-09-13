"""pylablib_instrument:

    This module implements the base class that all instrument drivers inherit. This base class, Instrument, generalizes
    the interaction with SPHEREx Test/Cal Instruments so that higher level software can interact with instruments in a
    standardized way.

Sam Condon, 06/30/2021
"""
import asyncio


class Instrument:

    def __init__(self, identifier=None):
        self.open_method = None
        self.identifier = identifier
        self.parameters = []
        self.get_methods = {}
        self.get_method_coros = {}
        self.getter_proc = None
        self.set_methods = {}
        self.set_method_coros = {}
        self.setter_proc = None

    def set_setter_proc(self, setter_proc):
        self.setter_proc = setter_proc

    def set_getter_proc(self, getter_proc):
        self.getter_proc = getter_proc

    def set_open_method(self, open_method):
        """set_open_method: set the open communication interface method

        :param open_method: function pointer that can be called to open
                            the communication interface
        :return:
        """
        self.open_method = open_method

    async def open(self):
        """open: open the communication interface by calling the previously set open_method()

        :return: communication interface object
        """
        if asyncio.iscoroutinefunction(self.open_method):
            ret = await self.open_method()
        else:
            ret = self.open_method()
        return ret

    def add_parameter(self, parameter_name, getter, setter, coro=False):
        """add_parameter: add functions to the getter and setter dictionaries for the specified parameter name.

        :param parameter_name: <string> name of parameter to be added.
        :param getter: <function object> function object corresponding to parameter getter.
        :param setter: <function object> function object corresponding to parameter setter.
        :return: None
        """
        if not coro:
            self.get_methods[parameter_name] = getter
            self.set_methods[parameter_name] = setter
        else:
            self.get_method_coros[parameter_name] = getter
            self.set_method_coros[parameter_name] = setter

        if parameter_name not in self.parameters:
            self.parameters.append(parameter_name)

    def add_get_parameter(self, parameter_name, getter, coro=False):
        """add_get_parameter: add function to the getter dictionary for the specified parameter name.

        :param parameter_name: <string> name of parameter to be added.
        :param getter: <function> function object corresponding to parameter getter.
        :return: None
        """
        if not coro:
            self.get_methods[parameter_name] = getter
        else:
            self.get_method_coros[parameter_name] = getter

        if parameter_name not in self.parameters:
            self.parameters.append(parameter_name)

    def add_set_parameter(self, parameter_name, setter, coro=False):
        """add_set_parameter: add function to the setter dictionary for the specified parameter name.

        :param parameter_name: <string> name of parameter to be added.
        :param setter: <function> function object corresponding to parameter setter.
        :return: None
        """
        if not coro:
            self.set_methods[parameter_name] = setter
        else:
            self.set_method_coros[parameter_name] = setter

        if parameter_name not in self.parameters:
            self.parameters.append(parameter_name)

    async def get_parameters(self, params):
        """get_parameters: return the specified instrument parameters as a dictionary

        :param params: string, list of strings, or "All" to specify which parameters
                       to query.
        :return: parameters dictionary
        """
        coro_list = {}
        return_dict = {}
        if params == 'All':
            for getter in self.get_methods:
                return_dict[getter] = self.get_methods[getter]()
            for getter in self.get_method_coros:
                coro_list[getter] = self.get_method_coros[getter]

        elif type(params) is list:
            for getter in params:
                if getter in self.get_methods:
                    return_dict[getter] = self.get_methods[getter]()
                elif getter in self.get_method_coros:
                    coro_list[getter] = self.get_method_coros[getter]
                else:
                    raise RuntimeError("Getter {} not found!".format(getter))

        elif type(params) is str:
            if params in self.get_methods:
                return_dict[params] = self.get_methods[params]()
            elif params in self.get_method_coros:
                coro_list[params] = self.get_method_coros[params]

        # Execute all getter coroutines ####
        for key in coro_list:
            get_task = asyncio.create_task(coro_list[key]())
            await get_task
            return_dict[key] = get_task.result()

        if self.getter_proc is not None:
            return_dict = self.getter_proc(return_dict)
        return return_dict

    async def set_parameters(self, params_dict):
        """set_params: set the specified parameters in the dialog display.

        :param params_dict: dictionary with keys and values of parameters to update
        :return: None
        """
        if self.setter_proc is not None:
            if asyncio.iscoroutinefunction(self.setter_proc):
                params_dict = await self.setter_proc(params_dict)
            else:
                params_dict = self.setter_proc(params_dict)
        else:
            coro_list = []
            func_list = []
            # Separate setters into coroutines and normal functions ######################
            for p in params_dict:
                if p in self.set_method_coros:
                    task = asyncio.create_task(self.set_method_coros[p](params_dict[p]))
                    coro_list.append(task)
                elif p in self.set_methods:
                    func_list.append((self.set_methods[p], params_dict[p]))
            ##############################################################################

            # Execute coroutines ###############################
            if len(coro_list) > 0:
                done, pending = await asyncio.wait(coro_list)
            ####################################################

            # Execute functions ################################
            # The above loop created a list of tuples of the format: (<function pointer>, <function parameters>)
            for func in func_list:
                func[0](func[1])
            ####################################################

    def start_measurement(self, *args, **kwargs):
        """Description: some instruments can read and return data. This method should be overridden by such instruments

        :return:
        """
        raise RuntimeError("start_measurement has not been overridden by a suitable measurement function.")

    def get_identifier(self):
        """get_identifier: get the instrument identifier string.

        :return: <string> instrument id
        """
        return self.identifier

    def set_identifier(self, new_id):
        """set_identifier: set the instrument identifier string.

        :param new_id: <string> instrument id
        :return: None
        """
        self.identifier = new_id




