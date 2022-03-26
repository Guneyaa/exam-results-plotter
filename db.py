import sqlite3
import os
import pandas as pd

import pendulum


class Database():
    def __init__(self, cwd):
        self.con = sqlite3.connect(os.path.join(cwd, 'db.sqlite3'))
        self.cwd = cwd
        self.cursor = self.con.cursor()
        self.init_tables()

    def init_tables(self):
        self.subjects = []
        self.n_tables = 0
        self.tables = self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'""").fetchall()
        for i in self.tables:
            if i[0].endswith('results'):
                self.subjects.append(i[0].replace('_results',''))
                self.n_tables += 1
        return self

    def create_tables(self, replace=False):
        print('initialising tables...')
        print('_'*30+'Enter "done" once all subjects are entered'+'_'*30)
        while True:
            subj = input('Enter subject name: ')
            if subj.upper() == 'DONE':
                break
            else:
                self.subjects.append(subj.upper())

        for i in self.subjects:
            if replace:
                sql = f'''DROP TABLE IF EXISTS {i}_results'''
                self.cursor.execute(sql)
            sql = f'''CREATE TABLE IF NOT EXISTS {i}_results
                            (id INTEGER, date TEXT, paper_topic TEXT, type TEXT, results DECIMAL(5,2), grade CHAR)'''
            self.cursor.execute(sql)
        self.init_tables()
        return self

    def enter_results(self):
        while True:
            print("TYPE IN 'RETURN' AND ENTER when done")
            subject = input(f"Select subject {self.subjects} or return?\n ||: ")
            if subject.upper() == 'RETURN':
                break
            elif subject.upper() in self.subjects:
                paper_topic = input("Enter paper topic: ")
                type = input("Enter paper type: ")
                marks_received = float(input("Enter mark received: "))
                out_of = float(input("Enter total achievable mark: "))
                date = pendulum.now().to_formatted_date_string()
                try:
                    id = int(self.cursor.execute('''SELECT * FROM "{}" ORDER BY id DESC LIMIT 1'''.format(subject.upper()+'_results')).fetchone()[0]) + 1
                except TypeError:
                    id = 1
                result = round((marks_received/out_of)*100, 2)
                grade = self.determine_grade(result)
                confirmation = input(f"Confirm record | {date} | {paper_topic} | {type} | results: {result} | grade: {grade} | {subject.upper()}\n(y/n)? : ")
                if confirmation.upper() == 'Y':
                    self.cursor.execute("""INSERT INTO "{}" VALUES (?,?,?,?,?,?)""".format(subject.upper()+'_results'), (id,date,paper_topic,type,result,grade))
                    print('Record added')
            else:
                print('invalid subject, select from {self.subjects} or make new subject table\n')
        self.con.commit()

    def exit(self):
        self.cursor.close()
        self.con.close()

    def read_data_to_DF(self, subject:str) -> pd.DataFrame:
        DF = pd.read_sql_table(f'{subject.upper()}_results', 'sqlite:///db.sqlite3')
        return DF

    def dump_all_into_DFdict(self) -> pd.DataFrame:
        dict = {}
        for i in self.subjects:
            DF = pd.read_sql_table(f'{i}_results', 'sqlite:///db.sqlite3')  # does not support sqlite dbapi connections, supports sqlalchemy connections
            dict.update({i:DF})     # needs sqlalchemy installed
        return dict

    def delete_database(self):
        # might hv to exit before this
        path = os.path.join(self.cwd, 'db.sqlite3')
        if os.path.exists(path):
            os.remove(path)
            print('DB removed')
        else:
            print('DB does not exist')

    def delete_table(self):
        table = input(f"Select subject table to drop\n{self.subjects} : ").upper() + '_results'
        self.cursor.execute("""DROP TABLE '{}'""".format(table))
        print(f'Dropped table {table}')
        self.init_tables()
        return self

    def backup_DB(self):
        pass

    @staticmethod
    def determine_grade(score):
        if score >= 90:
            return 'A+'
        elif 75 <= score < 90:
            return 'A'
        elif 65 <= score < 75:
            return 'B'
        elif 50 <= score < 65:
            return 'C'
        elif 35 <= score < 50:
            return 'S'
        else:
            return 'F'



# %%
if __name__ == '__main__':
    cwd = os.getcwd()
    db = Database(cwd)
    db.create_tables()
    db.enter_results()
    print(db.read_data_to_DF('chemistry'))

# %%
