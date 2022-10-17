# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:49:19 2022

@author: zakir
"""

import pandas as pd
import datetime as DT
import pickle

import io
import requests

pd.options.mode.chained_assignment = None

def One_day_dataframe(Current_date,model):
    """
    Loading data from google drive. Further, based on this data, important characteristics of the game session for 
    each player are calculated and combined into a daily dataframe
    """
      
    def download_link():
        """
        Function for compare current date and a link to google file
        """
        #Change the format of current date to operate with it
        file_index = Current_date.day - 1
        
        #Download file
        with open ('Links_to_google', 'rb') as fp:
            Links_list = pickle.load(fp)
        #Download file from the link
        url=Links_list[file_index]
        url='https://drive.google.com/uc?id=' + url.split('/')[-2]
        return url            
    url = download_link()

    while True:
        try:
            url2 = requests.get(url).text
            csv_raw = io.StringIO(url2)
            df = pd.read_csv(csv_raw)
            break
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            pass
    #Create dataframe for single user 
    User_list = df['client_user_id'].unique()

    def create(user_name):
        """Part responsible for creating dataframe with default user parameter"""
        Df1 = df[(df['client_user_id'] == user_name)]
        # convert 'timestamp' to date
        Df1['timestamp'] = pd.to_datetime(Df1['timestamp'],format='%Y-%m-%d %H:%M:%S')
        return Df1
    
    def fill():
        """Part responsible for creating dataframe with calculated parameters"""
        Df2 = pd.DataFrame(list(zip(User_list,Duration_list,Dropped_frames_list,FPS_list,FPS_std_list,Bitrate_list,RTT_list,RTT_std_list,Start_time_list,Device_list)),index = Sessions_list 
                                  , columns = ["User","Spended_time","Dropped_frames","FPS","FPS_std","Bitrate","RTT","RTT_std","Session beginning","Device"])
        return Df2
        
    class Session_parameters():
        """Class for creating lists of session's parameters for current user"""
        
        def __init__(self):   
            self.Df = create(user_id)
            self.sessions_list = self.Df["session_id"].unique() 
            self.spended_time = self.session_time()
            self.session_beginning = self.beginning_time()
            self.device = self.device_used()
            self.dropped = self.mean_values("dropped_frames")
            self.fps = self.mean_values("FPS")
            self.fps_std = self.std_values("FPS")
            self.bitrate = self.mean_values("bitrate")
            self.rtt = self.mean_values("RTT")
            self.rtt_std = self.std_values("RTT")
            self.user = self.user_ID()
       
        def session_time(self):
            #Session's duration
            sessions_time = []
            for i in range(len(self.sessions_list)):
                time = self.Df['timestamp'].where(self.Df['session_id'] == self.sessions_list[i]).max()-self.Df['timestamp'].where(self.Df['session_id'] == self.sessions_list[i]).min()
                sessions_time.append(int(time / pd.Timedelta(minutes=1)))               
            return sessions_time
         
        def beginning_time(self):
            #Session's beggining time
            sessions_beginning  = []
            for i in range(len(self.sessions_list)):
                time = self.Df['timestamp'].where(self.Df['session_id'] == self.sessions_list[i]).min()
                sessions_beginning .append(time)
            return sessions_beginning
       
        def device_used(self):
            #Device used for session
            user_devices = []
            for i in range(len(self.sessions_list)):
                user_devices.append(self.Df['device'].where(self.Df['session_id'] == self.sessions_list[i]).value_counts().idxmax())
            return user_devices
        
        def mean_values(self,feature_name):
            #Function for calculating mean values for dropped frames,fps,bitrate,rtt
            temp_list=[]
            for i in range(len(self.sessions_list)):
                temp = self.Df[feature_name].where(self.Df['session_id'] == self.sessions_list[i]).mean()
                temp_list.append(int(temp))
            return temp_list
        
        def std_values(self,feature_name):
            #Function for calculating mean values for dropped frames,fps,bitrate,rtt
            temp_list=[]
            for i in range(len(self.sessions_list)):
                temp = self.Df[feature_name].where(self.Df['session_id'] == self.sessions_list[i]).std(ddof=0)
                temp_list.append(int(temp))
            return temp_list   
        
        def user_ID(self):
            #List of the same user ID
            ID = []
            for i in range(len(self.sessions_list)):
                ID.append(user_id)
            return ID
        
        
    Day_df = pd.DataFrame()     #Data_frame contains one day data
    for user_id in User_list:
        
        Session_instance = Session_parameters()
        
        Sessions_list = Session_instance.sessions_list
        Duration_list = Session_instance.spended_time
        Start_time_list = Session_instance.session_beginning
        Device_list = Session_instance.device
        Dropped_frames_list = Session_instance.dropped
        FPS_list = Session_instance.fps
        FPS_std_list = Session_instance.fps_std
        Bitrate_list = Session_instance.bitrate

        RTT_list = Session_instance.rtt_std
        RTT_std_list = Session_instance.fps
        User_list = Session_instance.user
                
        client_df = fill()
        Day_df = pd.concat([Day_df,client_df])    
    
    Day_df = Day_df.sort_values(by=["User","Session beginning"])    
    Day_df.index.name = 'session_id'
    
    """ML"""
    cols = ['FPS', 'FPS_std', 'RTT', 'RTT_std', 'Dropped_frames']
    X_new = Day_df[cols].values
    Day_df["Stream_quality"] = model.predict(X_new)
    
    return Day_df
    
if __name__ == '__main__':
    #Print the date  from 01.09.2022     to 30.09.2022
    Current_date = '30/09/2022'
    Current_date = DT.datetime.strptime(Current_date,'%d/%m/%Y')
    Daily_df = One_day_dataframe(Current_date)    
    