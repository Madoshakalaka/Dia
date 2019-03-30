import threading
from enum import Enum
from typing import Dict, Optional




class TaskStat(Enum):
    STATIC = 0
    INPROGRESS = 1


class Task:

    indicator: Optional[threading.Event]
    stat: TaskStat
    allNeeds: Optional[Dict]
    name: str



    def __init__(self, name: str):
        self.name = name

        self.allNeeds = None

        self.stat = TaskStat.STATIC

        self.indicator = None



    def __call__(self, taskQueue, *args):

        if self.indicator is None:
            self.indicator = threading.Event()


        self.stat = TaskStat.INPROGRESS

        for need in self.allNeeds:
            subArgs = []

            need.indicator = threading.Event()

            for i in self.allNeeds[need]:
                subArgs.append(args[i])

            taskQueue.put((need, [taskQueue] + subArgs))

        for need in self.allNeeds:
            need.indicator.wait()


        self.doShit()

        self.indicator.set()
        self.stat = TaskStat.STATIC


    def doShit(self):
        indicator = threading.Event()

    def setAllNeeds(self, paraDict: dict):
        self.allNeeds = paraDict







# argNum = 1
acquireMeaning = Task("acquireMeaning")






