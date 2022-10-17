# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 23:26:24 2022

@author: zakir
"""

from threading import Thread
import time
import datetime as DT
import pandas as pd

import Try_builder
import Model
from class_menu import Menu as M

data_marker = 2

def File_downloader(current_date):
    global data_marker
    """Collecting data"""
    global Current_Df,data_marker,cur_date,model
    first_date = current_date
    data_marker = 0
    Df = pd.DataFrame()
    
    model = Model.LogRegression()
    model.load('model.pickle')
    
    while True:
        Current_Df = Df.copy()
        timeout = time.time() + 60*5   # 5 minutes from now                
        
        while time.time()<timeout:   
            Daily_df = Try_builder.One_day_dataframe(current_date,model)
            Df = pd.concat([Df,Daily_df])
            Df = Df.sort_values(by=["User","Session beginning"])
            
            if current_date == first_date:
                Current_Df = Df.copy()
                print("\nData from " + str(current_date.date()) + " was collected")
            data_marker = 1
        
            # cols = ['FPS', 'FPS_std', 'RTT', 'RTT_std', 'Dropped_frames']
            # X_new = Df[cols].values
            # model.train(X_new, Df['Stream_quality'].values)
            if timeout - time.time() > 0:
                time.sleep(timeout-time.time())
            else:
                break
        
        current_date += DT.timedelta(days=1)  
        cur_date = current_date
    
"Enter the date"
Current_date = '01/09/2022'
Current_date = DT.datetime.strptime(Current_date,'%d/%m/%Y')
cur_date = Current_date
th = Thread(target=File_downloader, args=(Current_date,))
th.start()

while True:
    if data_marker == 1:
        print("\n" + "Current date: " + cur_date.strftime("%Y_%m_%d"))
        print("Choose one operation from bellow")
        print("\t 1 : Get status for for the last 7 days")
        print("\t 2 : Print user summary")
        print("\t 3 : Predict user next session duration")
        print("\t 4 : Fetch new data and update users data and ML model")
        print("\t 5 : Get top 5 users based on time spent gaming")
        print("\t 6 : Exit program")
        menu_instance = M(Dataframe = Current_Df)
        
        try:
            i = int(input(" \tType here: "))
            if i==1:
                menu_instance.press1()
            elif i==2:
                menu_instance.press2()
            elif i==3:
                menu_instance.press3()
            elif i==4:
                menu_instance.press4()
            elif i==5:
                menu_instance.press5()
            elif i==6:
                menu_instance.press6()
        except ValueError:
            pass
        
        pass_var = input("Press (Enter) to continue")
    