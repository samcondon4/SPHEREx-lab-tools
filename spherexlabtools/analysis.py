""" This module provides the class, Spectrum, which can be used to streamline analysis with data recorded from the 
    SPHEREx spectral cal setup.

Sam Condon, 11/09/2021
"""

import numpy as np
import pandas as pd
import scipy.stats as spstats
from matplotlib.figure import Figure


class LinkedAttribute:
    """ Class implementing an individual linked attribute.
    """
    
    def __init__(self, **kwargs):
        """ Initialize the linked attribute.
        
        ## kwargs ##
        :param data: Data attribute.
        :param update: Method to update this attribute.
        :param next_attr: The attribute to update when this class' data attribute is set.
        """
        self.next_attr = None
        self.update_method = None
        self.data = None
        for key in kwargs:
            if key in self.__dict__:
                setattr(self, key, kwargs[key])
    
    def update(self, prev_data):
        """ Update the data attribute.
        
        :param prev_data: Data from the "parent" attribute.
        """
        if self.update_method is not None:
            self.data = self.update_method(prev_data)
    
    def __setattr__(self, name, value):
        """ Override the __setattr__ method to update next_attr is data is changed.
        """
        if name == "data" and self.next_attr is not None:
            object.__setattr__(self, "data", value)
            if type(self.next_attr) is list:
                for attr in self.next_attr:
                    attr.update(self.data)
            else:
                self.next_attr.update(self.data)
        else:
            object.__setattr__(self, name, value)


class Spectrum(object):
    """ This class loads a spectrum measured from the SPHEREx spectral cal setup and provides
        a set of basic operations that can be performed between spectra.
    """
              
    def __init__(self, **kwargs):
        """ Load a new spectrum from a csv
        """
        # raw data properties #
        self.raw = LinkedAttribute()
        self.raw.update_method = lambda fp: pd.read_csv(fp, comment="#")
        self.filepath = LinkedAttribute(next_attr=self.raw)
    
        # wavelength properties #
        self.wave_err = LinkedAttribute()
        self.waves = LinkedAttribute(update_method=lambda wdata: np.array(np.unique(wdata)))
        self.wavedata = LinkedAttribute(next_attr=self.waves,
                                         update_method=lambda wcol, df=self.raw: df.data[wcol].values)
        self.wavecol = LinkedAttribute(next_attr=self.wavedata)
        
        # power properties #
        self.power_err = LinkedAttribute(update_method=lambda pdata, wavedata=self.wavedata, waves=self.waves: \
                                         np.array([spstats.sem(p) for p in [pdata[np.where(wavedata.data == w)] for w in waves.data]]))
        self.power = LinkedAttribute(update_method=lambda pdata, wavedata=self.wavedata, waves=self.waves: \
                                     np.array([p.mean() for p in [pdata[np.where(wavedata.data == w)] for w in waves.data]]))
        self.powerdata = LinkedAttribute(next_attr=[self.power, self.power_err], 
                                         update_method=lambda pcol, df=self.raw: df.data[pcol].values)
        self.powercol = LinkedAttribute(next_attr=self.powerdata)
        
        # monochromator properties #
        self.slit_width = LinkedAttribute(next_attr=self.wave_err)
    
        # set key word arguments #
        for key in kwargs:
            if key in self.__dict__:
                setattr(self, key, kwargs[key])
    
    def plot(self, ax=None, fig_kwargs=None, ax_kwargs=None, errorbar_kwargs=None):
        """ Plot the waves and power properties in an error-bar plot.
        
        :param fig_kwargs: keyword arguments to send to the figure instantiation.
        :param ax_kwargs: keyword arguments to send to the axis instantiation.
        :param errorbar_kwargs: keyword arguments to send to the plotting method
        """
        # initialize keyword argument dictionaries #
        if type(fig_kwargs) is not dict:
            fig_kwargs = {}
        if type(ax_kwargs) is not dict:
            ax_kwargs = {}
        if type(errorbar_kwargs) is not dict:
            errorbar_kwargs = {}
        
        fig = None
        if ax is None:
            fig = Figure(**fig_kwargs)
            ax = fig.add_subplot(**ax_kwargs) 
            
        linear_yerr = self.power_err.data
        yerr = linear_yerr
        """
        # if plot is on a log scale, then move errors to log domain #
        if "yscale" in ax_kwargs and ax_kwargs["yscale"] == "log":
            relative_err = np.divide(self.power_err.data, self.power.data)
            print(relative_err)
            yerr = (1/np.log(10))*relative_err
        else:
            yerr = linear_yerr
        """
        
        ax.errorbar(x=self.waves.data, y=self.power.data, yerr=yerr, **errorbar_kwargs)
        
        return fig, ax
    
    def split(self, split_inds):
        """ Split the spectrum at the indices provided.
        
        :param split_inds: Indices at which the spectrum should be split.
        :return: List of new Spectrum objects corresponding to the splits. 
        """
        wavedata = [self.wavedata.data[split_inds[k]:split_inds[k+1]] for k in range(len(split_inds) - 1)]
        wavedata.append(self.wavedata.data[split_inds[-1]:])
        powerdata = [self.powerdata.data[split_inds[k]:split_inds[k+1]] for k in range(len(split_inds) - 1)]
        powerdata.append(self.powerdata.data[split_inds[-1]:])
        new_spects = [Spectrum(wavedata=wavedata[k], powerdata=powerdata[k]) for k in range(len(split_inds))]
        return new_spects
    
    def concat(self, spect):
        """ Concatenate two spectrum objects into a single new spectrum object.
        
        :param spect: Spectrum object to concatenate to self.
        :return: New Spectrum object containing the joined data.
        """
        new_spect = Spectrum()
        new_spect.raw = pd.concat([self.raw.data, spect.raw.data], axis=0)
        new_spect.wavecol = self.wavecol.data
        new_spect.powercol = self.powercol.data
        return new_spect
    
    def save(self, file_path, cols=None):
        """ Save wavelength, power, and power error data to a new csv located at file_path.
        
        :param file_path: directory path and filename of the csv to save.
        :param cols: provide column names for the saved csv. This should be a dictionary of the following form:
                         {
                             "Wavelength": <name for the wavelength column>,
                             "Power": <name for the power column>,
                             "Power SEM": <name for the power standard error of the mean column>
                         }
        """
        keys = {
            "Wavelength": "Wavelength",
            "Power": "Power",
            "Power SEM": "Power SEM"
        }
        if cols is not None:
            for k in cols:
                keys[k] = cols[k]
        data_dict = {}
        for k in keys:
            if k == "Wavelength":
                data = self.waves.data
            elif k == "Power":
                data = self.power.data
            elif k == "Power SEM":
                data = self.power_err.data
            data_dict[keys[k]] = data
        
        save_df = pd.DataFrame(data_dict)
        save_df.to_csv(file_path+".csv", index=False)
    
    ## ARITHMETIC OPERATORS #########################################################################################################
    def __truediv__(self, div_spect):
        """ Implements the division operator between spectra. This method takes the numpy arrays found in each spectra's power.data 
            attribute and returns a new Spectrum object whose power.data attribute equals the element-wise division of the spectra being
            divided.
        
        :param div_spect: Spectrum class to divide this class with.
        """
        new_spect = Spectrum()
        
        waves = self.waves.data
        if not np.equal(div_spect.waves.data, waves).all():
            raise RunTimeError("Wavelength data does not match!")
       
        new_spect.waves = waves
        new_spect.power = np.divide(self.power.data, div_spect.power.data)
        
        # uncertainty propagation #        
        new_spect.power_err = self.get_err(div_spect, "division", values=new_spect.power.data)
        
        return new_spect
    
    def __mul__(self, mult):
        """ Implements the multiplication operator between spectra, or a spectrum with a constant.
        
        :param mult: constant or spectrum to multiply by.
        """
        new_spect = Spectrum()
        new_spect.waves = self.waves.data
        if type(mult) is Spectrum:
            new_spect.power = np.multiply(self.power.data, mult.power.data)
            new_spect.power_err = self.get_err(mult, "multiplication", values=new_spect.power.data)
        else:
            new_spect.power = mult*self.power.data
            new_spect.power_err = mult*self.power_err.data
        
        return new_spect
    
    def get_err(self, element, operation, values=None):
        """ Returns the new 1 sigma error array after and operation is performed on a spectrum.
        
        :param element: object that the operation is being performed on with self.
        :param operation: operation between the objects.
        :param values: the new values after the operations was performed. Only required for the multiplication and division operation.
        """
        if operation == "division" or operation == "multiplication":
            self_err_percent = np.divide(self.power_err.data, self.power.data)*1e2
            lmnt_err_percent = np.divide(element.power_err.data, element.power.data)*1e2
            new_power_err_percent = np.add(self_err_percent, lmnt_err_percent)
            new_err = np.multiply(new_power_err_percent*1e-2, values)
        
        return new_err
            
    def __setattr__(self, name, value):
        """ Override of the __setattr__ method to work with the LinkedAttribute class.
        
        :param name: name of the attribute to set.
        :param value: value to set.
        """
        if not name in self.__dict__:
            self.__dict__[name] = value
        else:
            attr = self.__dict__[name]
            attr_type = type(attr)
            if attr_type is LinkedAttribute:
                setattr(attr, "data", value)
            else:
                object.__setattr__(self, name, value)
    
    
