import marshal
import pickle
import types

from task import Task


def doShit(repQueue, taskQueue, *args):
	repQueue.put("ignorant")


def test():
	acquireMeaning = Task('acquireMeaning', [])
	acquireMeaning.code = marshal.dumps(doShit.__code__)
	dd = {'acquireMeaning': acquireMeaning}


	with open("taskDict.pickle", 'wb') as file:
		pickle.dump(dd, file)




if __name__ == "__main__":
	test()
