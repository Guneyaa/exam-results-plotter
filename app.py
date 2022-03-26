from db import Database
from plot import Plotter

import os

cwd = os.getcwd()
db =  Database(cwd)
# READ DOCUMENTATION.MD for instructions to functions

print('PRESS CTRL+C TO EXIT')
while True:
    try:
        if db.n_tables == 0:
            print('PROCEEDING TO CREATING DATA TABLES')
            db.create_tables()
        choice = input("""
            PRESS CTRL+C TO EXIT\n
              [1] : Create new subject tables in database\n
              [2] : Enter results to subject tables\n
              [3] : Plot results of each subject table separately\n
              [4] : Plot results of all subjects together\n
              [5] : Plot specific table\n
              [6] : Delete DB and all records\n
              [7] : Delete specific table\n
              ENTER NUMBER ACCORDING TO REQUIRED COMMAND : """)
        if choice == '1':
            db.create_tables()
        elif choice == '2':
            db.enter_results()
        elif choice == '3':
            dfdict = db.dump_all_into_DFdict()
            plot = Plotter(dfdict, cwd)
            plot.plot_each()
        elif choice == '4':
            dfdict = db.dump_all_into_DFdict()
            plot = Plotter(dfdict, cwd)
            plot.plot_all_in_one()
        elif choice == '5':
            dfdict = db.dump_all_into_DFdict()
            plot = Plotter(dfdict, cwd)
            plot.plot_one()
        elif choice == '6':
            db.delete_database()
        elif choice == '7':
            db.delete_table()
        else:
            print('INVALID INPUT')
            
    except KeyboardInterrupt:
        db.exit()
        break
    