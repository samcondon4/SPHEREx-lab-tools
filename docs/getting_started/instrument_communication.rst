Instrument Communication
========================

PySxLab implements advanced control over several scientific instruments from various vendors. Before this control can be acheived, the low-level communication interface between each instrument must be established. The following subsections describe how to setup the various communication interfaces for the instruments that PySxLab controls.

* 'Heidenhain ND287, Linear Encoder Readout'_


Heidenhain ND287, Linear Encoder Readout
-----------------------------------------

PySxLab supports the RS-232 communication interface of the Heidenhain ND287. To configure this interface simply use a standard USB to RS-232 cable (ex. amazon_). Now follow the steps below to configure and verify that communication between your PC and the ND287 has been established:

#. Use the ND287 softkeys to navigate to the interface settings via **SETUP->INSTALL SETUP->INTERFACE SETTINGS** if at any point the device asks for a passcode, use: *95148*

#. Choose RS-232 for the serial port, then configure the serial communication settings to your liking. Note that PySxLab uses a default configuration of:
 
   * baud rate = 115200
   
   * data bits = 8
   
   * stop bits = 1
  
   * parity = None
  
   * Output tail = 1

   Should you desired to deviate from the default serial com configuration, make sure to update the communication field in your hardware configuration file.

.. _amazon: https://www.amazon.com/Adapter-Chipset%EF%BC%8CDB9-Serial-Converter-Windows/dp/B0759HSLP1/ref=asc_df_B0759HSLP1/?tag=hyprod-20&linkCode=df0&hvadid=459728334703&hvpos=&hvnetw=g&hvrand=17713210100510461256&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9031119&hvtargid=pla-997424051967&th=1
