Installation Guide
==================

Setting up Python
-----------------
The easiest way to get up and running with SPHERExLabTools is to use 
the `Anaconda Python Distribution`_. With this distribution, an independent Python environment
can be created that exactly matches a tested version of the code base. Follow the instructions
at the provided link to install the appropriate version of Anaconda for your operating system.


Setting up Git
--------------
To clone the SPHERExLabTools repository, Git_ must be installed. Follow the instructions at the
link provided to install the appropriate version of Git for your operating system.


Installing SPHERExLabTools
---------------------------
Clone the SPHERExLabTools repository with the following command in a bash shell::
        
        git clone --recurse-submodules https://github.com/SPHEREx/SPHEREx-lab-tools.git 

Next, navigate to the cloned repository and open the file *environment.yml* in your favorite text
editor. Edit the last line of this file where it says *prefix:* so that the value given here
matches the location of the *envs/* directory in your recently installed Anaconda_ installation
directory.

Now, execute the following command to create a new Anaconda_ environment that matches the tested version of the code base::
        
        conda env create --file=environment.yml

SPHERExLabTools integrates instrument drivers provided by the :pymeasure:`PyMeasure Project <>`. Significant contributions have been made to PyMeasure in the development of SPHERExLabTools and the most recent development version of PyMeasure is included in the SPHERExLabTools repository under *submodules/pymeasure*. To install this development version into the newly created Anaconda_ environment, first activate the environment with::

        conda activate spherexlabtools

Then navigate to *submodules/pymeasure* within the SPHERExLabTools repository and run::
        
        pip install -e .

Note that on Linux systems, the location of the *pip* binary within the *spherexlabtools* environment must be explicitly specified. This amounts to replacing the above call with something of the form::        
        /home/spherex-lab/anaconda3/envs/spherexlabtools/bin/pip install -e .


Installing Instrument Drivers
-----------------------------
SPHERExLabTools supports many standard instrument communication interfaces "out of the box", though
it will always be the case that certain vendors require specific driver installation procedures to
properly communicate with their instrument. Some helper documentation has been provided for a small set of instruments supported by SPHERExLabTools in :doc:`Instrument Communication <user_guide/instrument_communication>`. In most cases however, one must resort to the vendor provided documentation.

Next Steps
-----------

Now that you have installed SPHERExLabTools, you are ready use it! Check out :doc:`SPHERExLabTools Fundamentals <user_guide/fundamentals>` to get started!

.. _`Anaconda Python Distribution`: https://www.anaconda.com/products/individual
.. _Anaconda: https://www.anaconda.com/products/individual
.. _Git: https://git-scm.com/ 




