# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 13:17:29 2022

@author: zakir
"""

import pandas as pd
from datetime import datetime,timedelta
import sys

class Menu():
    def __init__(self,Dataframe):
        self.df = Dataframe
        self.convert()
        
    def convert(self):
        """Convert columns of dataframe to working formats"""
        self.df["Session beginning"] = pd.to_datetime(self.df["Session beginning"])
        self.df["User"] = self.df["User"].astype('str')
    
    def press1(self):
        """Function of creating summary"""
        def printer(Df):
            """Prints necessery things"""            
            string1 = "\nStatistics for the past 7 days:"
            print(string1)
            
            #Total sessions
            string2 = "\tTotal sessions: "+ str(Df.index.nunique())
            print(string2)  
            
            #Average time
            t_mean = Df["Spended_time"].mean()
            if t_mean <=60:
                str_time = str(int(t_mean)) + " minutes"
                string3 = "\tAverage time spent per session: " + str_time
                print(string3)
            else:
                str_time = str(int(t_mean//60)) + " hours " + str(int(t_mean%60)) + " minutes"
                string3 = "\tAverage time spent per session: " + str_time
                print(string3)
                
            #Total spended time
            t_total = str(int(Df["Spended_time"].sum()/60))
            string4 = "\tSum of hours spent by all users: " + t_total + " hours"
            print(string4)
            self.statistics_list = [string1,string2,string3,string4]
            return
            
        #Count how many days were between beggining and current session
        df2 = self.df.copy()
        df2["Session beginning"] = pd.to_datetime(df2["Session beginning"])
        df2 = self.df[df2["Session beginning"] >= (df2["Session beginning"]-timedelta(days=7))]
        printer(df2)
        return
    
    def press2(self):
        """Prints User's summary"""
        print("\nEnter user id:")
        user_id = str(input())
        # user_id = "086be3b2-31f6-4ed8-8076-d2696e2c5aa1"
        
        if user_id not in self.df["User"].tolist():
            print("User not found")
            return
        else:
            print("\nUser found!!")
            print(f"User with id : {user_id}")
            user_data = self.df[self.df['User'] == user_id]
            print("\nEnter period (yyyy/mm/dd - yyyy/mm/dd) :")
            playing_period = str(input())
            playing_period = playing_period.split(" - ", 2)
            start_date = playing_period[0]
            try:
                if start_date == "":
                    start_date = user_data.sort_values(by="Session beginning").iloc[0]["Session beginning"]
                    end_date = user_data.sort_values(by="Session beginning").iloc[-1]["Session beginning"]
                else:
                   end_date = playing_period[1]
                   start_date = datetime.strptime(start_date, '%Y/%m/%d')
                   end_date = datetime.strptime(end_date, '%Y/%m/%d')
                   # date_lower = datetime.strptime("2022/09/01", '%Y/%m/%d')
                   #date_upper = datetime.strptime("2022/09/30", '%Y/%m/%d')
                   if start_date > end_date:
                       print("There is no data in this period.")
                       return
            except ValueError:
                print("Wrong format of date. Try again.")
                return
            except TypeError:
                print("Wrong format of date. Try again.")
                return
            except IndexError:
                print("Wrong format of date. Try again.")
                return
                
            cur_user_data = user_data[
                (user_data["Session beginning"] >= start_date)
                & (user_data["Session beginning"] <= end_date)
            ]
            if len(cur_user_data) != 0:
                print("\tNumber of sessions :", len(cur_user_data))
                print(
                    "\tDate of first session :",
                    cur_user_data.sort_values(by="Session beginning").iloc[0]["Session beginning"].date(),
                )
                print(
                    "\tDate of most recent session :",
                    cur_user_data.sort_values(by="Session beginning").iloc[-1]["Session beginning"].date(),
                )
                print("\tAverage time spent per session :" +  str(int(cur_user_data["Spended_time"].mean())) + " min")
                print(
                    "\tMost frequently used device :",
                    cur_user_data["Device"].value_counts().index[0],
                )
                #TODO: beauty output
                print(
                    "\tDevices used :",
                    [dev for dev in cur_user_data["Device"].value_counts().index],
                )
                print("\tAvg RTT :", int(cur_user_data["RTT"].mean()))
                print("\tAvg FPS :", int(cur_user_data["FPS"].mean()))
                print("\tAvg dropped frames :", int(cur_user_data["Dropped_frames"].mean()))
                print("\tAvg bitrate :", int(cur_user_data["Bitrate"].mean()))
                print('\tTotal num of bad sessions: ', sum(cur_user_data["Stream_quality"] == 1))
                print("\tEstimated next session time :", str(int(cur_user_data["Spended_time"].mean())) + " min")
                
                #Check if SuperUser
                week_num = user_data["Session beginning"].dt.isocalendar().week
                is_su = (user_data.groupby(week_num)["Spended_time"].sum() > 60).any()
                print("Superuser :", "Yes" if is_su else "No")            
                
                """Option to find another user"""
                print("Find another user ? (yes/no)")
                choise = str(input())
                if choise == "yes":
                    self.press2()
                else:
                    return
            else:
                print("There are no games in this period.")
                return
    def press3(self):
        print("\nEnter user id:")
        user_id = str(input())    
        df2 = self.df[self.df["User"] == user_id]
        print("\tAverage session duration: ", str(int(df2["Spended_time"].mean())) + " min")
        return
    
    def press4(self):
        print("Data has been successfully updated")
        return
    
    def press5(self):
        # Function returns N largest elements
        def Nmaxelements(list1,list2, N):
            list_of_max = []
            max_users = []
         
            for i in range(0, N):
                max1 = 0
                for j in range(len(list1)):    
                    if list1[j] > max1:
                        max1 = list1[j]
                        max1_user = list2[j]
                
                list1.remove(max1)
                list2.remove(max1_user)                 
                list_of_max.append(max1)
                max_users.append(max1_user)
    
            return list_of_max,max_users
        users = []
        total_sum = []
        for user in self.df.User.unique():
            user_df = self.df[(self.df['User'] == user)]
            users.append(user)
            total_sum.append(user_df['Spended_time'].sum())
        print("\nTop 5 users:")
        User_times,Top_users = Nmaxelements(total_sum, users, 5)
        for i in range(5):
            hour = User_times[i] // 60
            minutes = User_times[i] % 60
            print("User: ",Top_users[i],"; "+" Time: ",hour,"hours",minutes,"minutes")
        return
    
    def press6(self):
        self.press1()
        summary = self.statistics_list
        print("Save summary ? (yes/no). Or another to back to the programm")
        choise = str(input())
        if choise == "no":
            print("Good bye!!")
            sys.exit()
        elif choise =="yes":
            date = self.df["Session beginning"].max()
            textfile = open(str(date.date()) + "_summary.txt", "w")
            for element in summary:
                textfile.write(element + "\n")
            textfile.close()
            print("Good bye!!")
            sys.exit()
        else:
            pass