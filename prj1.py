# -------------------------------------------libraries--------------------------------
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
# import descartes
import pyodbc
import numpy as np
import sys
from copy import copy
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar
import time




# ---------------------------main query----------------------------------
def main_query(qmin, qmax):
    #process_label['text'] = "please wait..."
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:/WSU FY2012 OP.mdb;')
    cursor = conn.cursor()

    # --------------------SQL command--------
    # example inputs to test the query:
    a_v_min = "V140"
    # a_v_min =
    a_v_max = "V230"
    a_e_min = "E140"
    a_e_max = "E230"
    a_min = 140
    a_max = 230
    # -------------------progress bar---------
    #progress.place(relwidth=0.9, relheight=0.06, relx=0.6, rely=0.7)


    #time.sleep(5)

    #------------------------------------------

    sql_command='''SELECT [FIPS County Code Table].[County Name], 
    Count([FIPS County Code Table].[County Name]) AS [Count]  
    FROM ([WSU_OP_Diagnosis] INNER JOIN [WSU_OP_Demographics] 
    ON [WSU_OP_Diagnosis].CNTRL = [WSU_OP_Demographics].CNTRL) 
    INNER JOIN [FIPS County Code Table] ON [WSU_OP_Demographics].statecounty = [FIPS County Code Table].FIPS_Code 
    WHERE  ((([FIPS County Code Table].State)='Kansas') 
    AND (([WSU_OP_Diagnosis].DIAG)> ? And ([WSU_OP_Diagnosis].DIAG)< ?)) 
    GROUP BY [FIPS County Code Table].[County Name]ORDER BY [FIPS County Code Table].[County Name];
     '''
    # ----------------------------

    cursor.execute(sql_command, (a_min, a_max))

    for row in cursor.fetchall():
        print(row)

       # my_window.update()
    # remember to add a Progressbar later
    #progress.stop()
    #progress.grid_forget()
# -------------------------making the window------------------------

my_window = Tk()
# my_canvas = Canvas(my_window, width=500, height=200, background='white')
my_canvas = Canvas(my_window, background='white')
# my_canvas.grid(row=3, column=0)
my_window.geometry("500x500")

# progress = Progressbar(my_window, orient=HORIZONTAL,length=300)
# progress.grid(row=5, column=0,padx=40, pady=20)


# -------------function run_query()---------called by button 1--------


# (result1, result2) = choices.get(key, ('default1', 'default2'))

def run_query():
    #progress.start()
    variable = my_combobox.get()
    (result1, result2) = choices.get(variable, ('default1', 'default2'))
    process_label['text'] = "please wait..."
    main_query(result1, result2)

    # print(result1)
    # print(result2)


# ----------------label------------------------
process_label = ttk.Label(my_window,text=" ")
process_label.grid(row=4, column=0,padx=40, pady=20)
#process_label['text']="asda"
# ---------------------- label ------------------------
combo_label = ttk.Label(my_window, text="select diseases of: ")
# combo_label.grid(row=0,sticky="")
# combo_label.place(relwidth=0.7, relheight=0.3, relx=0.3, rely=0.2)
# lable_sep=ttk.Separator(my_window,orient="horizontal")
combo_label.grid(row=0, column=0,padx=40, pady=20)

# ----------------------combo box------------------------


deases_lst = ['infectious and parasitic diseases',
              'neoplasms',
              'endocrine, nutritional and metabolic diseases, and immunity disorders',
              'diseases of the blood and blood-forming organs',
              'mental disorders',
              'diseases of the nervous system',
              'diseases of the sense organs',
              'diseases of the circulatory system(Heart Related)',
              'diseases of the respiratory system',
              'diseases of the digestive system',
              'diseases of the genitourinary system',
              'complications of pregnancy, childbirth, and the puerperium',
              'diseases of the skin and subcutaneous tissue',
              'diseases of the musculoskeletal system and connective tissue',
              'congenital anomalies',
              'certain conditions originating in the perinatal period',
              'symptoms, signs, and ill-defined conditions',
              'injury and poisoning']

choices = {'infectious and parasitic diseases': (1, 1399),
           'neoplasms': (140, 2399),
           'endocrine, nutritional and metabolic diseases, and immunity disorders': (240, 2799),
           'diseases of the blood and blood-forming organs': (280, 2899),
           'mental disorders': (290, 3199),
           'diseases of the nervous system': (320, 3599),
           'diseases of the sense organs': (360, 3899),
           'diseases of the circulatory system(Heart Related)': (390, 4599),
           'diseases of the respiratory system': (460, 5199),
           'diseases of the digestive system': (520, 5799),
           'diseases of the genitourinary system': (580, 6299),
           'complications of pregnancy, childbirth, and the puerperium': (630, 6799),
           'diseases of the skin and subcutaneous tissue': (680, 7099),
           'diseases of the musculoskeletal system and connective tissue': (710, 7399),
           'congenital anomalies': (740, 7599),
           'certain conditions originating in the perinatal period': (760, 7799),
           'symptoms, signs, and ill-defined conditions': (780, 7999),
           'injury and poisoning': (800, 9999)
           }

my_str_var = tk.StringVar()
my_combobox = ttk.Combobox(my_window, textvariable=my_str_var, values=deases_lst)
my_combobox.grid(row=1, column=0,padx=40, pady=20)
#my_combobox.place(relwidth=0.6, relheight=0.05, relx=0.3, rely=0.4)

# ----------------------button DB1------------------------

button1 = ttk.Button(my_window, text="Show Results  from DB1",
                     command=lambda: run_query())
button1.grid(row=2, column=0, padx=40, pady=20)
#button1.place(relwidth=0.28, relheight=0.06, relx=0.3, rely=0.5)
# ------------------button DB1 & DB2-----------------------
# measureSystem = StringVar()
button2 = ttk.Button(my_window, text='Show Results from both',
                     command=lambda:run_query())
#button2.place(relwidth=0.3, relheight=0.06, relx=0.6, rely=0.5)
button2.grid(row=2, column=1, padx=10)
# ----------------------running ----------------------

my_window.mainloop()

# --------------------------------------------------------
gdf = gpd.read_file('GU_CountyOrEquivalent.shp')
df = pd.DataFrame(gdf)
df_seg = pd.read_csv("seg.csv")
new_df = df[df["State_Name"] == 'Kansas']
new_df.reset_index(drop=True, inplace=True)
merge_df = pd.merge(new_df, df_seg, left_on='County_Nam', right_on='County', how='inner')

gdf2 = gpd.GeoDataFrame(merge_df)

gdf2['coords'] = gdf2['geometry'].apply(lambda x: x.representative_point().coords[:])
gdf2['coords'] = [coords[0] for coords in gdf2['coords']]

# print(gdf.shape)
# print(gdf.head())
# gdf2.plot(column='County_Nam')

print(gdf2.head())
plt.rcParams['figure.figsize'] = (20, 15)
ax = gdf2.plot(column='Segment')
gdf2.apply(lambda x: ax.annotate(s=x.County_Nam, xy=x.geometry.centroid.coords[0], ha='center'), axis=1)
# plt.show()

seg2 = merge_df[['County_Nam', 'Segment']]
print(merge_df[['County_Nam', 'Segment']])
seg2.to_csv('seg2_out.csv', encoding='utf-8')
# new_df.to_csv('new-df.csv',encoding='utf-8')
print(new_df.head())


