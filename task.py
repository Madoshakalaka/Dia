import marshal
import threading
import types
from enum import Enum
from queue import Queue
from typing import Dict, Optional


class TaskStat(Enum):
	STATIC = 0
	INPROGRESS = 1


class Task:
	code: bytes
	indicator: Optional[threading.Event]
	stat: TaskStat
	allNeeds: Optional[Dict]
	name: str

	def __init__(self, name: str, allNeeds=None):
		self.name = name

		if allNeeds is None:
			self.allNeeds = []
		else:
			self.allNeeds = allNeeds

		self.stat = TaskStat.STATIC

		self.indicator = None

		# code of the function the task does
		self.code = None

		# proper function
		self.function = None

	def __call__(self, repQueue:Queue, taskQueue, *args):

		# create indicator for initiating task
		if self.indicator is None:
			self.indicator = threading.Event()

		self.stat = TaskStat.INPROGRESS

		# wait for requirements to finish
		for need in self.allNeeds:
			subArgs = []

			need.indicator = threading.Event()

			for i in self.allNeeds[need]:
				subArgs.append(args[i])

			taskQueue.put((need, [repQueue, taskQueue] + subArgs))

		for need in self.allNeeds:
			need.indicator.wait()

		# do what else needs to be done
		self.doShit(repQueue, taskQueue, *args)

		# signals the task has been done
		self.indicator.set()
		self.stat = TaskStat.STATIC

	# noinspection PyArgumentList
	def doShit(self, repQueue, taskQueue, *args):
		if self.function is None:
			f = types.FunctionType(marshal.loads(self.code), globals(), "function")
			self.function = f

			self.function(repQueue, taskQueue, *args)
		else:
			self.function(repQueue, taskQueue, *args)

	def setAllNeeds(self, paraDict: dict):
		self.allNeeds = paraDict



# argNum = 1
acquireMeaning = Task("acquireMeaning", [])
