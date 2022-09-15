Output Data Standard
#####################

| While SPHERExLabTools supports output to many file types, the principles of how experiment data is organized for
  archival are common to all types. As described in :ref:`Fundamentals <user_guide/fundamentals:Fundamentals>`, data
  is generated and sent out for archival via :ref:`Procedures <user_guide/fundamentals:Procedures>`. Generally, procedures
  generate a single data point while :ref:`Procedure Sequences <user_guide/fundamentals:Procedure Sequences>` string together
  multiple procedures in a loop to generate a larger data set.

| Single data points are referred to as **Records** while collections of data points are **Record Groups**.

| In addition to the measured quantities of interest (voltage, temperature, images, etc.), Records contain all experiment
  information such as instrument metadata, procedure parameters, timestamps, etc., associated with the measured quantity.
  Each piece of information contained within a Record is placed into one of 3 categories:

    1. **Data**: The measured quantities of the experiment.
    2. **Procedure Parameters**: Parameters of the procedure that generated the measured quantities.
    3. **Metadata**: Other relevant information about the state of the experiment and the instruments within the experiment testbed.

| For any given output filetype, these pieces of information are separated but linked together via two indices called *RecordGroup*
  and *RecordGroupInd*. *RecordGroup* is an integer identifying a set of records that are grouped together, for instance after being
  generated from the same Procedure Sequence. *RecordGroupInd* identifies unique records within a larger Record Group.

Default Metadata:
-----------------

Example:
--------

| Let's consider an example using the fake experiment generated in the :ref:`Step-by-Step Experiment Configuration <tutorials/stepbystep_config:Step-by-Step Experiment Configuration>`
  tutorial.

| In this experiment, the temperature of a cryostat baseplate is monitored in response to some input voltage applied to a heater. Additionally, the thermal emission of
  the heater is monitored via an IR camera.

  The measured quantities of the experiment are:

    - Baseplate temperature (K)
    - Heater IR emission intensity (mW)
    - Heater measured input voltage (V)
    - Timestamp at which quantities are measured (YYYYMMDD_HHMMSS.ms)

  The parameters of the Procedure recording the above information are:

    - Heater input voltage (V)
    - Sample Time (s)
    - Sample Rate (hz)

  Other metadata relevant to the experiment are:

    - Cryostat pressure (Torr)
    - Camera gain

| Now lets take a look at the data generated for each of the three categories after a few measurements.

1) 10 seconds of data at 1 hz
******************************

| Suppose that to start, our cryostat baseplate temperature is stable at 40K. Then, we apply 5V. to the heater input and record
  data every second for 10 seconds. Our procedure parameters then look like:

    - Heater input voltage = 5
    - Sample Time = 10
    - Sample Rate = 1

| After the procedure completes its 10 seconds of data collection, we will have three tables generated corresponding to the three categories
  **1. Data**, **2. Procedure Parameters**, and **3. Metadata**. These tables will look something like:

  **1. Data:**

    .. figure:: fig/Data_rg0.png

        Data table after the first measurement.

  **2. Procedure Parameters**

    .. figure:: fig/PP_rg0.png

        Procedure parameters table after the first measurement.

  **3. Metadata**

    .. figure:: fig/Meta_rg0.png

        Metadata table after the first measurement.

