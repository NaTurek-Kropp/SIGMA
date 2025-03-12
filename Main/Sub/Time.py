import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from Main import Data


timestamps = [None] * Data.NumOfQuestions('ProjectData/pytania.txt')

def StartTimer():
    return time.time()

def EndTimer(startTime, questionIndex):
    endTime = time.time()
    elapsedTime = endTime - startTime
    timestamps[questionIndex] = (round(elapsedTime, 2))

def TimeStamps():
    return timestamps

def GetTotalTime():
    total_time = sum(filter(None, timestamps))
    return round(total_time, 2)