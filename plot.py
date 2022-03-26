import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt


class Plotter():
    def __init__(self, df_dict: dict, cwd:str, DF: pd.DataFrame = None):
        self.dict = df_dict
        if DF is not None:
            self.df = DF
        os.makedirs(os.path.join(cwd, 'plots'), exist_ok=True)
        self.dir = os.path.join(cwd, 'plots')
        
    def plot_each(self):
        for key in self.dict:
            temp_list = []
            df = self.dict[key]
            for idx, i in df.iterrows():
                temp_list.append(round(i['results']))
            y = np.array(temp_list)
            plt.plot(y, marker='o')
            plt.xlabel('paper_number')
            plt.ylabel('results')
            plt.grid(axis='x')
            plt.title(f"Exam_results: {key.replace('_results', '')}")
            plt.savefig(os.path.join(self.dir, f'{key}_plot.png'), bbox_inches='tight')
            plt.show()
        print('PLOTS SAVED')

    def plot_all_in_one(self):
        for key in self.dict:
            temp_list = []
            df = self.dict[key]
            for idx, i in df.iterrows():
                temp_list.append(round(i['results']))
            y = np.array(temp_list)
            plt.plot(y, marker='o')
        plt.title(f"Exam_results: {[ i.replace('_results', '') for i in self.dict ]}")
        plt.xlabel('paper_number')
        plt.ylabel('results')
        plt.grid(axis='x')
        plt.savefig(os.path.join(self.dir, 'full_plot.png'), bbox_inches='tight')
        print('PLOT SAVED')
        plt.show()
        
    def plot_one(self):
        print([key for key in self.dict])
        table_name = input('Enter subject name to be plotted: ')
        temp_list = []
        for idx,i in self.dict[table_name.upper()].iterrows():
            temp_list.append(round(i['results']))
        y = np.array(temp_list)
        plt.plot(y, marker='o')
        plt.title(f"Exam_results {table_name.upper()}")
        plt.xlabel('paper_number')
        plt.ylabel('results')
        plt.grid(axis='x')
        plt.savefig(os.path.join(self.dir, f'{table_name.upper()}_plot.png'), bbox_inches='tight')
        print('PLOT SAVED')
        plt.show()
        
