import time

timestamps = []

def StartTimer():
    return time.time()

def EndTimer(startTime):
    endTime = time.time()
    elapsedTime = endTime - startTime
    timestamps.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(endTime)))
    return elapsedTime
