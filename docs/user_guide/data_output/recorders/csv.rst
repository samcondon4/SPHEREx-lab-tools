Comma-Separated-Values (CSV)
#############################

| The CsvRecorder class merges the **Data**, **Procedure Parameters** and **Metadata** tables into a single table using
  the *RecordGroup* and *RecordGroupInd* indices. In the merged table, **Procedure Parameter** column labels have 'proc' prepended,
  while **Metadata** column labels are prepended with 'meta'.

| Using the tables generated in :ref:`Output Data Standard Example <user_guide/data_output/standard:Example>`, the merged table
  that would be written to a csv would look something like the following:

.. raw:: html
    :file: merged_table.html
