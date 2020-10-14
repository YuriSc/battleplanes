import time
from ExecTime import startTimer
from ExecTime import getTimerStat
for i in range(5):
    t1 = startTimer("t1")
    t2 = startTimer("t2")
    time.sleep(0.1)
    t2.stop()
    t1.stop()
for q in getTimerStat():
    print(f"{q[0]}: at all={q[1][0]}, avg={q[1][0]/q[1][1]}")

print(*getTimerStat(), sep='\n')
# for q in getTimerStat():
#     print(q)
#
# def myp(i1, i2):
#     print(repr(i1), repr(i2))

#print(map(lambda x: print(x**2), [1, 2, 3, 4]))
print("#######")
list(map(print, getTimerStat()))

list(map(
    lambda q: print(f"{q[0]}: at all={q[1][0]}, avg={'N/A' if q[1][1] == 0 else q[1][0] / q[1][1]}"),
    getTimerStat()))

# print(*getTimerStat(), sep='\n')
import csv
with open('eggs.csv', 'a', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Spam'] * 5 + ['Baked "Beans"'])
    csv_writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
