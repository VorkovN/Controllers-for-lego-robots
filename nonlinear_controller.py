#!/usr/bin/python3
# coding=utf-8
from ev3dev.ev3 import *
import math

mB = LargeMotor('outB')
mC = LargeMotor('outC')
f = open('lab6.txt', 'w')
f.write('0' + ' ' + '0' + '\n')
mB.position = 0
mC.position = 0
masx = [1, -1, -1, 1]
masy = [1, 1, -1, -1]
x1 = 0
y1 = 0
a1 = 0
al2 = 0
ar2 = 0
r = 0.0275
B = 0.19
ar1 = 0
al1 = 0
k = 10
t2 = 0
v_max = 300
try:
    for i in range(len(masx)):
        while True:
            t1 = time.time()
            dt = t1 - t2

            al1 = mB.position
            ar1 = mC.position
            a1 += math.radians((ar1 - ar2) - (al1 - al2)) * r / B
            x1 += math.cos(a1) * math.radians((ar1 - ar2) + (al1 - al2)) * r / 2
            y1 += math.sin(a1) * math.radians((ar1 - ar2) + (al1 - al2)) * r / 2

            p = math.sqrt(math.pow(x1 - masx[i], 2) + math.pow(y1 - masy[i], 2))
            a = math.atan2(masy[i] - y1, masx[i] - x1) - a1

            v = v_max * math.tanh(p) * math.cos(a)
            w = k * a + v_max * math.tanh(p) / p * math.sin(a) * math.cos(a)
            f.write(str(x1) + ' ' + str(y1) + ' ' + str(dt))
            if p < 0.2:
                break

            if w > 20:
                w = 20
            if w < -20:
                w = -20

            if v > 80:
                v = 80
            if v < -80:
                v = -80

            mB.run_direct(duty_cycle_sp=v - w)
            mC.run_direct(duty_cycle_sp=v + w)

            t2 = t1
            ar2 = ar1
            al2 = al1
finally:
    mB.stop(stop_action='brake')
    mC.stop(stop_action='brake')
    f.close

