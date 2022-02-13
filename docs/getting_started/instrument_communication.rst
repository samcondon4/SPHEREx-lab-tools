.. _getting-started_instrument-communication:
Instrument Communication
========================

SpherexLabTools implements advanced control over several scientific instruments from various vendors. Before this control can be acheived, the low-level communication interface between each instrument must be established. The following subsections describe how to setup the various communication interfaces for the instruments that PyLabTools controls.

.. _resource-name-id:

Resource Name Identification:
------------------------------
To communicate with instruments, SpherexLabTools uses instrument classes implemented in our `forked version of pymeasure`_, which in turn uses the pyvisa_ library under the hood. In **pyvisa**, instruments are identified on a computer by a **resource name**. To identify the resource name for an instrument, make sure it is the only piece of hardware plugged into the usb port and execute the following code in a python interactive session:

.. code:: python

        import pyvisa as pv

        rm = pv.ResourceManager()
        print(rm.list_resources())

Heidenhain ND287, Linear Encoder Readout:
------------------------------------------

SpherexLabTools supports the RS-232 communication interface of the Heidenhain ND287. To configure this interface simply use a standard USB to RS-232 cable (ex. amazon_). Now follow the steps below to configure and verify that communication between your PC and the ND287 has been established:

#. Use the ND287 softkeys to navigate to the *Interface Settings* menu via **SETUP->INSTALL SETUP->INTERFACE SETTINGS** if at any point the device asks for a passcode, use: *95148*

#. Choose RS-232 for the serial port, then configure the serial communication settings to your liking. Note that SpherexLabTools uses a default configuration of:
 
   * baud rate = 115200
   
   * data bits = 8
   
   * stop bits = 1
  
   * parity = None
  
   * Output tail = 1

   Should you desired to deviate from the default serial com configuration, make sure to update the communication field in your hardware configuration file.

#. To verify that the interface between your computer and the ND287 is sound, open a terminal-emulator program such as TeraTerm or HyperTerminal and open up the COM port associated with the USB to RS232 adapter. Set up the serial port settings to match those of the previous step. Next, navigate to the *Import/Export* menu via **SETUP->IMPORT EXPORT** then press **EXPORT**. If everything is configured properly you should see a whole slew of information echoed within the terminal emulator.  

.. _`forked version of pymeasure`: https://github.com/samcondon4/pymeasure
.. _pyvisa: https://pyvisa.readthedocs.io/en/latest/
.. _amazon: https://www.amazon.com/Adapter-Chipset%EF%BC%8CDB9-Serial-Converter-Windows/dp/B0759HSLP1/ref=asc_df_B0759HSLP1/?tag=hyprod-20&linkCode=df0&hvadid=459728334703&hvpos=&hvnetw=g&hvrand=17713210100510461256&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9031119&hvtargid=pla-997424051967&th=1


