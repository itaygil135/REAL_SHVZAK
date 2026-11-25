

#An Israeli Queue is a modified FIFO queue with the following key features:
#Items are enqueued with both a value and a group ID.
#New items can join existing groups, inserting after the last item of that group.
#Dequeuing removes and returns all items from the first group in the queue.
#API
#Enqueue(data Object, groupID int): Add an item to the queue with a group ID.
#Dequeue() List<Object>: Remove and return all items from the first group.

from datetime import datetime, timedelta
from collections import *
import queue
import sys
import math
import random

COMMANDERS = r"C:\itay_private\schduale mission\commanders.txt"
SOLDIERS = r"C:\itay_private\schduale mission\soldiers.txt"

# class soldier():
#     def __init__(self):
#         self._is_here = True

#     def setSoldierApperence(self):
#         self._is_here = not self._is_here

class Node:
    def __init__(self,soldier):
        self.soldier_name = soldier
        self.next = None
        self.prev = None
        self.is_here = True
        #timeToGOVacation = #TODO need to get as an argument


    def setSoldierApperence(self):
        self._is_here = not self._is_here
    

    


class specialQueue:
    def __init__(self,listOfSoldiers = None):
        self.__head = None
        self.__tail = None
        self.dict_nameString_toNode = {}
        if listOfSoldiers != None:
            for soldier in listOfSoldiers:
                newSoldier = Node(soldier)
                self.append(newSoldier)


    
    def append(self,soldier):
         
        if self.__head == None and self.__tail == None:
            self.__head = soldier
            self.__tail = soldier
        else:
            self.__tail.next = soldier
            soldier.prev = self.__tail
            self.__tail = soldier

        self.dict_nameString_toNode[soldier.soldier_name] = soldier



    def popleft(self):
        back = None
        if not (self.__head == None and self.__tail == None):
            back = self.__head
            if self.__head == self.__tail:
                self.__head = None
                self.__tail = None
            else:
                self.__head = self.__head.next
                self.__head.prev = None
            back.next = None
        return back




    def pop(self,soldierName = None):
        if self.__head == None and self.__tail == None:
            return None

        if self.__head == self.__tail:
            if soldierName != None and soldierName != self.__head.soldier_name:
                return None
            back = self.__tail
            self.__tail = None
            self.__head = None
            return back
        
        if soldierName != None:
            required_soldier = self.__dict_nameString_toNode.get(soldierName)
            notInQueue = (required_soldier.prev == None and required_soldier.next == None)
            if notInQueue:
                return None
            if required_soldier.soldier_name == self.__head.soldier_name:
                return self.popLeft()
            if required_soldier.soldier_name != self.__tail.soldier_name:
                required_soldier.next.prev = required_soldier.prev
                required_soldier.prev.next = required_soldier.next
                required_soldier.next = None
                required_soldier.prev = None
                return required_soldier

        #I am not doing else for saving double code the case that soldier name equal 
        # last soldier gonna be handle also with the regular pop
        back = self.__tail
        self.__tail = self.__tail.prev
        self.__tail.next = None
        back.prev = None
        return back



    def pushFront(self,soldierNode):
        if self.__head == None and self.__tail == None:
            self.__head = soldierNode
            self.__tail = soldierNode

        else:
            soldierNode.next = self.__head
            self.__head.prev = soldierNode
            self.__head = soldierNode
        


            
        
class Mission():
    def __init__(self,mission_name,time_of_the_mission,amount_of_commandors,amount_of_simple_soldiers,startDay,endDay,endMission):
            self._mission_name = mission_name
            self._time_of_the_mission = time_of_the_mission
            self._amount_of_commandors = amount_of_commandors
            self._amount_of_simple_soldiers = amount_of_simple_soldiers
            self._list_of_soldiers = []
            self.beginTimeAtDay = startDay
            if endDay.hour < startDay.hour or (endDay.hour == startDay.hour and endDay.minute <= startDay.minute):
                endDay = endDay+ timedelta(days=1)
            self.endTimeAtDay = endDay
            self.start_week_date = startDay
            self.end_week_date = endMission

            self.fromHouer = startDay
            self.toHouer = self.beginTimeAtDay + timedelta(hours=self._time_of_the_mission[0],minutes=self._time_of_the_mission[1])
    
    def getMission(self):
        return self._mission_name

    def getTimeOfMission(self):
        return self._time_of_the_mission
    
    def getAmountOfComadors(self):
        return self._amount_of_commandors
    
    def getAmountOfSimpleSoldiers(self):
        return self._amount_of_simple_soldiers
    
    def getListOfSoldiers(self):
        return self._list_of_soldiers
    
    def setListOfSoldiers(self):
        self._list_of_soldiers = []

    
    def __lt__(self, other):
        return self._time_of_the_mission[0] + self._time_of_the_mission[1] < other._time_of_the_mission[0] +other._time_of_the_mission[1] 
    
    def getBeginDay(self):
        return self.beginTimeAtDay
    
    def getEndDay(self):
        self.endTimeAtDay

    def getStartWeekDate(self):
        return self.start_week_date

    def getEndWeekDate(self):
        return self.end_week_date
    
    def getFromHouer(self):
        return self.fromHouer
    
    def getToHouer(self):
        return self.toHouer
    
    # def SetFromHouer(self,hour):
    #         self._fromHouer = hour

    def setToHouer(self):
        self.toHouer = self.fromHouer + timedelta(hours=self._time_of_the_mission[0],minutes=self._time_of_the_mission[1])

    

class Schduale():
    
    def __init__(self):
        self._commandors_queue = specialQueue()
        self._soldiers_queue = specialQueue()
        self._days = 0
        self._missions_deatails = []
        self._missions_ends = {} # key is hour value is list which holds the indexes at the 'missions' list of the missions which end at that houer
        self._mission_we_have = set()
        self._timeTOVaction = {}
        self._timeTOComeBack = {}
        self._current_time = None
        self._beginDate = None
        self._end_date = None
        #self._time_to_name = {}



    def addAnewSoldier(self):
        name = input("please give his name ")
        #TODO asking for his vacation time out and back and maybe when he going to join


    def giveMeInput(self,command_soldiers,simple_soldiers):
        while True:
            length_of_schduale = input("please give me the amount of days you want me to perpare a schduale (it should be at the format: '1' or '2' etc..) ")
            if length_of_schduale.isdigit() == False:
                print("you didnt choose at the right format please choose again (it should be at the format: '1' or '2' etc..) ")
            else:
                self._days = int(length_of_schduale)
                #TODO some graphich which ask for the start date and hour
                # meanwhile we will make 
                now = datetime.now()
                self._beginDate = (now + timedelta(days=1)).replace(hour=0, minute=0)
                self._current_time = self._beginDate
                self._end_date= self._beginDate + timedelta(days=self._days)
                break
        #print("I AM OUT!!")

        while (True):
            there_is_mission = "0"
            mission_name = ""
            time_of_the_mission = -5
            amount_of_commandors = 0
            amount_of_simple_soldiers = 0
            beginFirstTime = None
            endLastTime = None
            isCircle = False
            total_commandors = 0
            total_simple_soldiers = 0


            while True:
                there_is_mission = input("if there is more mission press: 1, otherwise press: 2 ")
                if there_is_mission != "1" and there_is_mission != "2":
                    print("you chosed unvalid option! the only option is '1' for adding a mission and '2' for not, please choose again ")
                else:
                    break
                
            if there_is_mission == "2":
                break
            
            while (True):
                mission_name = input("please write the mission name ")
                print(" ")
                print(" ")
                if mission_name in self._mission_we_have:
                    print("there is already exist such a mission with that name so give me another name ")
                    print(" ")
                    print(" ")
                else:
                    break

            while (True):

                hour_input = input("Please write the hour you want the mission to begin (HH:mm): ")
                minute_input = input("Please write the minutes at the hour you want the mission to begin (HH:mm): ")
                if hour_input.isdigit() == False or minute_input.isdigit() == False:
                    print("you did not write a digit please choose again ")
                    print(" ")
                    print(" ")
                    continue
                if int(hour_input) > 23 or int(minute_input) > 59:
                    print("unvalid hour")
                    print(" ")
                    print(" ")
                
                beginFirstTime = self._current_time.replace(hour=int(hour_input),minute=int(minute_input))
                break

            while (True):

                hour_input = input("please write the last hour that this mission that at each day (HH:mm): ")
                minute_input = input("Please write the minutes at the hour you want the mission to end each day (HH:mm): ")
                if hour_input.isdigit() == False or minute_input.isdigit() == False:
                    print("you did not write a digit please choose again ")
                    print(" ")
                    print(" ")
                    continue
                if int(hour_input) > 23 or int(minute_input) > 59:
                    print("unvalid hour")
                    print(" ")
                    print(" ")
                
                endLastTime = self._current_time.replace(hour=int(hour_input),minute=int(minute_input))
                break



            while (True):
                num_of_commandors = input("plese write the amount of comandors the mission demands (it should be at the format: '1' or '2' etc..) ")
                print(" ")
                print(" ")
                if num_of_commandors.isdigit() == False:
                    print("you did not write an option from the right format please choose again at the correct format ")
                    print(" ")
                    print(" ")
                else:
                    amount_of_commandors =int(num_of_commandors)
                    total_commandors+=amount_of_commandors
                    break
                
            while(True):
                num_of_simple_soldiers = input("plese write the amount of simple soldiers the mission demands (it should be at the format: 1 (not One)  or 2 (not Two) etc..) ")            
                print(" ")
                print(" ")
                if num_of_simple_soldiers.isdigit() == False:
                    print("you did not write an option from the right format please choose again at the correct format ")
                    print(" ")
                    print(" ")
                else:
                    amount_of_simple_soldiers = int(num_of_simple_soldiers)
                    total_simple_soldiers+=amount_of_simple_soldiers
                    break    
            
            while (True):
                is_houer = input("plese write the amount of hours the mission demands, the options is:beetwin 0 to 24 it should be at the format: 1 (not One)  or 2 or 3 etc..) ")
                is_minutes = input("plese write the amount of minutes the mission demands, the options is:beetwin 0 to 59 it should be at the format: 1 (not One)  or 2 or 3 etc..) ")

                print(" ")
                print(" ")

                if is_houer.isdigit() == False or is_minutes.isdigit() == False:
                    print("you did not write a digit please choose again ")
                    print(" ")
                    print(" ")
                    continue
                time_of_the_mission = (int(is_houer),int(is_minutes))
                if (time_of_the_mission[0] > 24) or (time_of_the_mission[0] < 0) or (time_of_the_mission[1] > 59) or (time_of_the_mission[1] < 0)  :
                    print("you did not chosed from the option I gave you! choose again ")
                    print(" ")
                    print(" ")
                elif time_of_the_mission[0] == 0 and time_of_the_mission[1] == 0:
                    print("it is not posible that the length of a mission will be 0 hours and 0 minutes so please choose again ")
                else:
                    break

   
            # Now I support just mission of all weeks if they all day and if they are not all day but in the future addd should be also support half weeks and cte..
            missionWeeksEnds = beginFirstTime + timedelta(days=7)
            if not (beginFirstTime.hour == endLastTime.hour and beginFirstTime.minute == endLastTime.minute):
                missionWeeksEnds-= timedelta(days=1)
            missionWeeksEnds= missionWeeksEnds.replace(hour=endLastTime.hour,minute=endLastTime.minute)
            if missionWeeksEnds > self._end_date:
                missionWeeksEnds = self._end_date
            self._missions_deatails.append(Mission(mission_name,time_of_the_mission,amount_of_commandors,amount_of_simple_soldiers,beginFirstTime,endLastTime,missionWeeksEnds)) #should be the real finish of the mission
            
            if (len(command_soldiers) == total_commandors or len(simple_soldiers) == total_simple_soldiers):
                print("I do not allwod that the amount of soldiers all missions demends will needed all the soldiers there is So start from the begining I delelte all what we did besdides the length of the schduale")
                self._mission_we_have.clear()
                self._missions_deatails = []




        
        self._missions_deatails.sort()

        #TODO some graphich which let fill the name of imple soldiers and commander and of course the dates they needs to go out and come back(option to do it weekly) give option of out and back just by days and hours but not option to detail by minutes and secondes
        # meanwhile we will use the TXT files

        self._commandors_queue = specialQueue(command_soldiers)
        self._soldiers_queue = specialQueue(simple_soldiers) 
        



    def printDeateils(self,mission,currTime):
        ind = 0
        lst =  mission.getListOfSoldiers()
       
        if len(lst) != 0:
            filename = f"day{currTime}.txt"
            # with open(filename, "a") as file:
            #     file.write(f"at mission: {mission.getMission()} at range of hours: {mission.getFromHouer()} until {mission.getToHouer()} the occupied soldiers are: ")
            #     #to delete
            formatted_time_from = mission.fromHouer.strftime("%H:%M")
            formatted_time_to = mission.toHouer.strftime("%H:%M")
        

            MidNight = (mission.fromHouer + timedelta(days=1)).replace(hour=0,minute=0)
            daysChange = mission.toHouer > MidNight and mission.fromHouer < MidNight
            if daysChange:
                #TODO write to txt fille of curTime - timedelta(days=1)
                print("at mission: ",mission.getMission()," at range of hours: 00:00 until ",formatted_time_to," the occupied soldiers are: ")
            elif mission.toHouer == MidNight:
                pass #do nothing beacuse the part at the hand will handle this
            else:
                print("at mission: ",mission.getMission()," at range of hours: ",formatted_time_from," until ",formatted_time_to," the occupied soldiers are: ")


            #TODO write : 
            while ind < mission.getAmountOfComadors()+mission.getAmountOfSimpleSoldiers():
                # with open(filename, "a") as file:
                #     file.write(f"{lst[ind]} ")
                    #to delete
                if not (mission.toHouer == MidNight):
                    print(lst[ind].soldier_name," ")
                #TODO write  lst[ind] + space  

                
                if ind < mission.getAmountOfComadors():
                    self._commandors_queue.append(lst[ind])
                else:
                    self._soldiers_queue.append(lst[ind])
                ind+=1


            print(" ")
            #TODO write new line
            #print(mission.getListOfSoldiers())
            mission.setListOfSoldiers()
            #print(mission.getListOfSoldiers())
            #lst = mission.getListOfSoldiers()
        





    def updateDeteilsHours(self,index,currTime):
            flag = False
            mission = self._missions_deatails[index]
            # over = False
            if mission.getEndWeekDate() == currTime:
                if mission.getEndWeekDate() !=  mission.start_week_date  +  timedelta(days=7):
                    flag = True
                mission.end_week_date = mission.end_week_date +  timedelta(days=7)
                mission.start_week_date = mission.start_week_date  +  timedelta(days=7)



                mission.beginTimeAtDay = mission.start_week_date
                mission.endTimeAtDay = mission.beginTimeAtDay.replace(hour=mission.endTimeAtDay.hour, minute=mission.endTimeAtDay.minute) + timedelta(days=1)
                if not (mission.endTimeAtDay.hour < mission.beginTimeAtDay.hour or (mission.endTimeAtDay.hour == mission.beginTimeAtDay.hour and mission.endTimeAtDay.minute <= mission.beginTimeAtDay.minute)):
                    mission.endTimeAtDay = mission.endTimeAtDay -  timedelta(days=1)
                mission.fromHouer = mission.beginTimeAtDay
                mission.setToHouer()
                if flag:
                    if mission.fromHouer not in self._missions_ends:
                        self._missions_ends[mission.fromHouer] = [index]
                    else:
                        self._missions_ends[mission.fromHouer].append(index)
                    return False
                
            # check = mission.beginTimeAtDay.replace(hour=mission.endTimeAtDay.hour(), minute=mission.endTimeAtDay.minute()) + timedelta(days=1)
            elif currTime == mission.endTimeAtDay:
                if not (currTime.hour == mission.beginTimeAtDay.hour and currTime.minute == mission.beginTimeAtDay.minute):
                    flag = True
                mission.beginTimeAtDay = mission.beginTimeAtDay + timedelta(days=1)
                mission.endTimeAtDay = mission.endTimeAtDay + timedelta(days=1)
                mission.fromHouer = mission.beginTimeAtDay
                mission.setToHouer()
                if flag:
                    if mission.fromHouer not in self._missions_ends:
                        self._missions_ends[mission.fromHouer] = [index]
                    else:
                        self._missions_ends[mission.fromHouer].append(index)
                    return False


            else:  
                    mission.fromHouer = mission.toHouer
                    mission.setToHouer()

            return True




    def fillMission(self,index,mission):
        lst =  mission.getListOfSoldiers()
        numComand = 0
        numSoldiers = 0
        while numComand < mission.getAmountOfComadors():
            lst.append(self._commandors_queue.popleft())
            numComand+=1

        while numSoldiers < mission.getAmountOfSimpleSoldiers():
            lst.append(self._soldiers_queue.popleft())
            numSoldiers+=1
        
        if mission.getToHouer() not in self._missions_ends:
            self._missions_ends[mission.getToHouer()] = [index]
        else:
            self._missions_ends[mission.getToHouer()].append(index)





    def updateMissionSoldiers(self,index,currTime):
        mission = self._missions_deatails[index]
        numComand = 0
        numSoldiers = 0
        ind = 0
        lst =  mission.getListOfSoldiers()


        if len(lst) != 0:
            filename = f"day{currTime}.txt"
            # with open(filename, "a") as file:
            #     file.write(f"at mission: {mission.getMission()} at range of hours: {mission.getFromHouer()} until {mission.getToHouer()} the occupied soldiers are: ")
            #     #to delete

            formatted_time_from = mission.fromHouer.strftime("%H:%M")
            formatted_time_to = mission.toHouer.strftime("%H:%M")


            MidNight = (mission.fromHouer + timedelta(days=1)).replace(hour=0,minute=0)
            daysChange = mission.toHouer > MidNight and mission.fromHouer < MidNight
            if daysChange:
                #TODO write to txt fille of curTime - timedelta(days=1)
                print("at mission: ",mission.getMission()," at range of hours: 00:00 until ",formatted_time_to," the occupied soldiers are: ")
            elif mission.toHouer == MidNight:
                pass #do nothing beacuse the part at the hand will handle this
            else:
                print("at mission: ",mission.getMission()," at range of hours: ",formatted_time_from," until ",formatted_time_to," the occupied soldiers are: ")

            

            #TODO write : 
            while ind < mission.getAmountOfComadors()+mission.getAmountOfSimpleSoldiers():
                # with open(filename, "a") as file:
                #     file.write(f"{lst[ind]} ")
                    #to delete
                if not (mission.toHouer == MidNight):
                    print(lst[ind].soldier_name," ")
                #TODO write  lst[ind] + space  

                
                if ind < mission.getAmountOfComadors():
                    self._commandors_queue.append(lst[ind])
                else:
                    self._soldiers_queue.append(lst[ind])
                ind+=1


            print(" ")
            #TODO write new line
            #print(mission.getListOfSoldiers())
            mission.setListOfSoldiers()
            #print(mission.getListOfSoldiers())
            lst = mission.getListOfSoldiers()
            flag = False
            # over = False
            if mission.getEndWeekDate() == currTime - timedelta(days=1):
                print("days before")
            #TODO TO CHECK WHY IT IS NOT WORKED IN A PARILALY MISSION IN A DAY WHEN THE LENGTH OF SCHDUALE IS LONGER THAN 7 DAYS
            if mission.getEndWeekDate() == currTime:
                if mission.getEndWeekDate() !=  mission.start_week_date  +  timedelta(days=7):
                    flag = True
                mission.end_week_date = mission.end_week_date +  timedelta(days=7)
                mission.start_week_date = mission.start_week_date  +  timedelta(days=7)



                mission.beginTimeAtDay = mission.start_week_date
                mission.endTimeAtDay = mission.beginTimeAtDay.replace(hour=mission.endTimeAtDay.hour, minute=mission.endTimeAtDay.minute) + timedelta(days=1)
                if not (mission.endTimeAtDay.hour < mission.beginTimeAtDay.hour or (mission.endTimeAtDay.hour == mission.beginTimeAtDay.hour and mission.endTimeAtDay.minute <= mission.beginTimeAtDay.minute)):
                    mission.endTimeAtDay = mission.endTimeAtDay -  timedelta(days=1)
                mission.fromHouer = mission.beginTimeAtDay
                mission.setToHouer()
                if flag:
                    if mission.fromHouer not in self._missions_ends:
                        self._missions_ends[mission.fromHouer] = [index]
                    else:
                        self._missions_ends[mission.fromHouer].append(index)
                    return
                
            # check = mission.beginTimeAtDay.replace(hour=mission.endTimeAtDay.hour(), minute=mission.endTimeAtDay.minute()) + timedelta(days=1)
            elif currTime == mission.endTimeAtDay:
                if not (currTime.hour == mission.beginTimeAtDay.hour and currTime.minute == mission.beginTimeAtDay.minute):
                    flag = True
                mission.beginTimeAtDay = mission.beginTimeAtDay + timedelta(days=1)
                mission.endTimeAtDay = mission.endTimeAtDay + timedelta(days=1)
                mission.fromHouer = mission.beginTimeAtDay
                mission.setToHouer()
                if flag:
                    if mission.fromHouer not in self._missions_ends:
                        self._missions_ends[mission.fromHouer] = [index]
                    else:
                        self._missions_ends[mission.fromHouer].append(index)
                    return


            else:  
                    mission.fromHouer = mission.toHouer
                    mission.setToHouer()


        # takeVacatinTimeCommandors  = []
        # takeVacatinTimeSolldiers = []

        while numComand < mission.getAmountOfComadors():
            # if self._commandors_queue.peek().timeToGoVacation < mission.fromHouer:
            #     takeVacatinTimeCommandors.append(self._commandors_queue.popleft())
            #     continue
            lst.append(self._commandors_queue.popleft())
            numComand+=1
        # for com in reversed(takeVacatinTimeCommandors):
        #     self._commandors_queue.pushFront(com)

        while numSoldiers < mission.getAmountOfSimpleSoldiers():
            # if self._soldiers_queue.peek().timeToGOVacation < mission.fromHouer:
            #     takeVacatinTimeSolldiers.append(self._soldiers_queue.popleft())
            #     continue
            lst.append(self._soldiers_queue.popleft())
            numSoldiers+=1
        # for com in reversed(takeVacatinTimeCommandors):
        #     self._commandors_queue.pushFront(com)
        
        if mission.getToHouer() not in self._missions_ends:
            self._missions_ends[mission.getToHouer()] = [index]
        else:
            self._missions_ends[mission.getToHouer()].append(index)
        

        formatted_time_from = mission.fromHouer.strftime("%H:%M")
        MidNight = (mission.fromHouer + timedelta(days=1)).replace(hour=0,minute=0)
        if mission.toHouer >= MidNight:
            print("at mission: ",mission.getMission()," at range of hours: ",formatted_time_from," until 00:00 the occupied soldiers are: ")
            for soldier in lst:
                print(soldier.soldier_name)
            print("")
            print("")







    # def takeOut(self,soldier,queue):
    #     if soldier.is_here == True:
    #         queue.pop(soldier.soldier_name)
    #     else:
    #         queue.pushFront(soldier)

    #     soldier.setSoldierApperence()
    #     soldier.timeToGOVacation = soldier.timeToGOVacation + timedelta(days=7)    
            


    def makeMeScheduale(self):
        last = self._current_time - timedelta(days=1)
        filename = f"day{self._current_time}.txt"

        for ind,mission in enumerate(self._missions_deatails):
            init = mission.getBeginDay()
            if init not in self._missions_ends:
                self._missions_ends[init] = [ind]
            else:
                self._missions_ends[init].append(ind)


        # Open the file using 'with', which handles closing the file automatically

        while (self._current_time < self._end_date):
            if last.date() != self._current_time.date():
                last = self._current_time        
                filename = f"day{self._current_time}.txt"
                # with open(filename, "w") as file:
                #     file.write(f"Schduale for day  {self._current_time} .\n")
                #     #to delete
                print("Schduale for day ",self._current_time,".")
                print(" ")
                print(" ")

                    # file.write("\n")
                    # file.write("\n")



            # if self._current_time in self._timeTOVaction:
            #     for soldier_name in self._timeTOVaction.get(self._current_time):
            #         if soldier_name in self._commandors_queue.dict_nameString_toNode:
            #             self.takeOut(self._commandors_queue.dict_nameString_toNode(soldier_name),self._commandors_queue)
            #         else:
            #             self.takeOut(self._soldiers_queue.dict_nameString_toNode(soldier_name),self._soldiers_queue)

            if self._current_time in self._missions_ends:
                while len(self._missions_ends.get(self._current_time)) > 0:    
                    index = self._missions_ends.get(self._current_time).pop()
                    # mission = self._missions_deatails[index]
                    # fill = (len(mission.getListOfSoldiers()) == 0)
                    # self.printDeateils(mission,self._current_time)
                    # if self.updateDeteilsHours(index,self._current_time):
                    #     self.fillMission(index,self._missions_deatails[index])

                    self.updateMissionSoldiers(index,self._current_time)
                del self._missions_ends[self._current_time]
                         


            self._current_time = self._current_time + timedelta(minutes=1)
        
        for i,finishMission in enumerate(self._missions_deatails):
            if finishMission.getFromHouer() < self._current_time:
                self.printDeateils(finishMission,finishMission.getToHouer())
                self.updateDeteilsHours(i,finishMission.getToHouer())

        #self._missions_ends.clear()




        





    def run(self,command_soldiers,simple_soldiers):
        self.giveMeInput(command_soldiers,simple_soldiers)
        self.makeMeScheduale()






def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    


def readFile(file_path,my_list):
    try:
        # Reading the file line by line
        with open(file_path, 'r') as file:
            for soldier in file:
                my_list.append(soldier.strip())  # List comprehension to add lines to a list
        
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        my_list = ["error"]
        
    except Exception as e:
        print(f"An error occurred: {e}")
        my_list = ["error"]
    
    if len(my_list) == 0:
        my_list = ["empty"]

    return my_list



if "__main__" == __name__:
    if len(sys.argv) != 1:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    command_soldiers = readFile(COMMANDERS,[]) #readFile(sys.argv[1],[])
    simple_soldiers = readFile(SOLDIERS,[]) #readFile(sys.argv[2],[])
    if command_soldiers[0] == "error" or  simple_soldiers == "error":
        print("there is an error in one of the file's ")
        sys.exit(1)
    elif command_soldiers[0] == "empty" or  simple_soldiers == "empty":
        print("there is no commandors or soldiers so the mission is unpoosible to occupied ")
        sys.exit(1)


    random.shuffle(command_soldiers)  # Shuffles in place
    random.shuffle(simple_soldiers)  # Shuffles in place
    schduale = Schduale()
    schduale.run(command_soldiers,simple_soldiers)

    #TODO remember to add a check that we are not alowd at any time that not gonn have at least double 2 soldiers than the peak of the soldiers the mission demands
    #
    # TODO after the mission finish to make a scduale can run all the mission and if there mission 
    #       that her  start week date  is smaller than the end date of scudale so update also the start week date and also the end week date
    #   of the mission to be bigger at 7 days and write as a txt file kind PCA at OS
    
    #   TODO if the user ask for running by the previus scduale check that the start end week of all the mission is not smaller than current time
    # TODO to make sure that each start week date is the same as the the date the beginfirst of mission initlize at the constructor 
    #       (the same as the end week date to (beginfirstTime + timedelta(7)).replace(hour=endFirstTime.hour,minute=endFirstTime.minute) 
    #           of each mission) also to make sure that at the GUI we are allowd to the user to pick weeky and daily option and if he chose
    #           for example weeky but not daily so to make sure we let him just valid options of picking the hours of last mission end
    #            depends at which day 
