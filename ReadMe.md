# Exam results DB and plotting tool

## Methods and functions

### Database

refer db.py

- ``create_tables`` function to initialise DB or add new tables.
- ``enter_results`` to enter records into DB.
- ``read_data_into_df`` , ``dump_all_into_df`` dumps records from DB into pandas dataframe.
- ``exit`` to exit DB connection.
- ``delete_database`` to delete DB file (deletes all records).
- ``delete_table`` to drop indivdual tables

### Plotter

refer plot.py

- ``plot_each`` to plot every table in DB separately (saves copies in png).
- ``plot_all_in_one`` to plot all records in DB on one graph (saves copies in png).
- ``plot_one`` to plot a specified subject table.