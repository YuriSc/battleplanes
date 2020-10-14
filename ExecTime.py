
"""
Save time elapsed to execution
"""

import time
from collections import defaultdict


class Timer:
    def __init__(self, accum):
        self.accum = accum
        self.start_time = time.perf_counter_ns()

    def start(self) -> None:
        self.start_time = time.perf_counter_ns()

    def stop(self):
        result = time.perf_counter_ns() - self.start_time
        self.accum.add(result)
        return result


class TimerAccumulator:
    def __init__(self):
        self.accumulator = 0.0
        self.count = 0

    def add(self, time):
        self.accumulator += time
        self.count += 1

    def get(self):
        return self.accumulator, self.count

    def createTimer(self):
        return Timer(self)


class TimerManager:
    timers = defaultdict(TimerAccumulator)

    @staticmethod
    def startTimer(timer_name:str) -> Timer:
        return TimerManager.timers[timer_name].createTimer()

    @staticmethod
    def getStat():
        return [(key, TimerManager.timers[key].get()) for key in TimerManager.timers]


def startTimer(timer_name:str) -> Timer:
    return TimerManager.startTimer(timer_name)


def getTimerStat():
    return TimerManager.getStat()