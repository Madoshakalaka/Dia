import logging
import pickle
import queue
import threading
import time
from sys import stderr
from typing import List, Dict, Optional

import dialogBox
from pattern import *
import os.path

# 算1+1
from task import Task

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setupLogger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

sumupLogger = setupLogger("sumupLogger", "sumups.log")



dialogQueue = queue.Queue()
outQueue = queue.Queue()

taskQueue = queue.Queue()


wordDict: Dict[str, WordDef]
formDict: Dict[WordForm, WordDef]
upperCateDict: Dict[WordCategory, Tuple[WordCategory]]
lowerCateDict: Dict[WordCategory, Tuple[WordCategory]]
taskDict: Dict[str, Task]


if os.path.isfile("upperCateDict.pickle"):
    with open("upperCateDict.pickle", "rb") as f:
        upperCateDict= pickle.load(f)
else:
    print("upperCateDict.pickle not fould, empty upperCateDict created", file=stderr)
    upperCateDict= dict()

if os.path.isfile("taskDict.pickle"):
    with open("taskDict.pickle", "rb") as f:
        taskDict= pickle.load(f)
else:
    print("taskDict.pickle not fould, empty taskDict created", file=stderr)
    taskDict = dict()


if os.path.isfile("lowerCateDict.pickle"):
    with open("lowerCateDict.pickle", "rb") as f:
        lowerCateDict= pickle.load(f)
else:
    print("lowerCateDict.pickle not fould, empty lowerCateDict created", file=stderr)
    lowerCateDict= dict()

if os.path.isfile("wordDict.pickle"):
    with open("wordDict.pickle", "rb") as f:
        wordDict = pickle.load(f)
else:
    print("wordDict.pickle not fould, empty wordDict created", file=stderr)
    wordDict = dict()

if os.path.isfile("formDict.pickle"):
    with open("formDict.pickle", "rb") as f:
        formDict = pickle.load(f)
else:
    print("formDict.pickle not fould, empty formDict created", file=stderr)
    formDict = dict()




expectations: List[SenPattern] = [vnImperative]

newWordsLearned = []

dialogHandlers: List = list()

def main():
    uiExited = threading.Event()
    thinkThread = threading.Thread(target=mainLoop, args=(uiExited,))


    thinkThread.start()
    dialogBox.initialize()



    uiExited.set()

    thinkThread.join()

    quit()


def factorMatch(factor: DefFactor, testDef: WordDef)->bool:

    if factor.factorRelation is FactorRelation.ISTYPE:

        types = testDef.types
        return types is not None and factor.type in types

    else:
        raise Exception("Not implemented")





def compDefMatch(compDef: CompDef, testDef: WordDef)->bool:

    allFactorPass = True

    for factor in compDef.factors:
        if not factorMatch(factor, testDef):
            allFactorPass = False
            break

    return allFactorPass

# def relationCheck(partition: List[str], relations: List[Relation]) -> bool:
#     allPass = True
#
#     for relation in relations:
#         if relation.relationType is RelationType.vnMatch:
#             pass


def isSubCate(c1: WordCategory, c2: WordCategory) -> bool:
    return c2 in upperCateDict[c1]

def checkUsage(pattern: SenPattern, partition: List[WordDef]):

    del pattern

    end = len(partition)
    anyDefPass = False

    for i, wordDef in enumerate(partition):




        for wordUsage in wordDef.usages:

            catePass = True
            for j in range(end):
                rel = j-i

                # todo
                if rel != 0 and not isSubCate(partition[j].category, wordUsage.segments[rel]):

                    catePass = False
                    break

            if catePass:
                anyDefPass = True
                break

        if anyDefPass:
            break


    return anyDefPass





def parse(c:str)->Optional[WordDef]:

    if c in wordDict:
        return wordDict[c]
    else:
        results = []
        for form, wordDef in formDict.items():
            if form.match(c):
                results.append(wordDef)

        num = len(results)

        if num == 0:
            return None
        elif num == 1:
            return results[0]
        else:
            raise Exception("not implemented")




def parsePartition(p: List[str]) -> List[WordDef]:
    pp: List[WordDef] = []

    for c in p:
        pp.append(parse(c))
    return pp



def tryMatch(exp: SenPattern, dialog: str) -> List[List[str]]:

    matches = []

    for partition in partitionGen(dialog, len(exp)):

        parsedPartition = parsePartition(partition)

        # not fully understanding the proposed parts
        if None in parsedPartition:
            pass

        else:

            allPass = True

            for i, comp in enumerate(parsedPartition):
                compDef = exp[i]

                if not compDefMatch(compDef, comp):
                    allPass = False
                    break

            if allPass:

                anyUsagePass = checkUsage(exp, parsedPartition)

                if anyUsagePass:

                    raise Exception("not implemented")

                # relationResult = relationCheck(partition, exp.relations)
                # if relationResult:
                #     matches.append(partition)

    return matches




def dealWith(dialog: str):
    results = []
    nonTrivialCounter = 0

    for exp in expectations:

        result = tryMatch(exp, dialog)

        if result:
            # print("hey: %s"% result)
            results.append(result)
            nonTrivialCounter += 1

    # print(results)

    if nonTrivialCounter != 0:
        raise(Exception("not implemented"))

    else:
        # todo
        taskQueue.put((taskDict["acquireMeaning"], (taskQueue, dialog)))



def mainLoop(uiExited):

    while not uiExited.is_set():

        rec = dialogBox.yieldAll()
        if rec:
            while rec:
                dialogQueue.put(rec.pop(0))

        else:
            pass

        try:
            dialog = dialogQueue.get(False)
        except queue.Empty:
            pass

        else:
            # print(dialog)
            threading.Thread(target=dealWith,args = (dialog,)).start()


        try:
            rep = outQueue.get(False)
        except queue.Empty:
            pass
        else:
            dialogBox.postAsSur(rep)

        try:
            taskPair = taskQueue.get(False)

        except queue.Empty:
            pass
        else:
            threading.Thread(target=taskPair[0], args = taskPair[1]).start()



        time.sleep(0.05)

    with open("wordDict.pickle", "wb") as ff:
        pickle.dump(wordDict, ff)

    with open("formDict.pickle", "wb") as ff:
        pickle.dump(formDict, ff)

    with open("upperCateDict.pickle", "wb") as ff:
        pickle.dump(upperCateDict, ff)

    with open("lowerCateDict.pickle", "wb") as ff:
        pickle.dump(lowerCateDict, ff)

    with open("taskDict.pickle", "wb") as ff:
        pickle.dump(taskDict, ff)

    # sumupLogger.info("\n")
    # sumupLogger.info("new words learned: %s"% newWordsLearned)
    # sumupLogger.info("\n")




if __name__ == "__main__":
    main()
