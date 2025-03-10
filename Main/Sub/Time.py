import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from Main import Data


timestamps = [None] * Data.NumOfQuestions('Data/pytania.txt')

def StartTimer():
    return time.time()

def EndTimer(startTime, questionIndex):
    endTime = time.time()
    elapsedTime = endTime - startTime
    timestamps[questionIndex] = (elapsedTime)

def TimeStamps():
    return timestamps
