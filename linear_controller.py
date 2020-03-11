#!/usr/bin/python3
# coding=utf-8
from ev3dev.ev3 import *
import math

mB = LargeMotor('outB')
mC = LargeMotor('outC')
f = open('lab5.txt', 'w')
f.write('0' + ' ' + '0' + '\n')
mB.position = 0
mC.position = 0
kp1 = 20
kp2 = 100 
masx = [500, -500, -500, 500,500, -500, -500, 500, 500]
masy = [500, 500, -500, -500,500, 500, -500, -500, 500]
x1 = 0
y1 = 0 
a1 = 0
al2 = 0
ar2 = 0
r = 27.5
B = 153
Up = 0
Uv = 0
ar1 = 0
al1 = 0
P = 40
V = 60
k = 1

try:
    for i in range(len(masx)):
        while True:
            dist = math.sqrt(math.pow(x1 - masx[i], 2) + math.pow(y1 - masy[i], 2))
            X = (masx[i] - x1) * math.cos(a1) + (masy[i] - y1) * math.sin(a1)
            Y = (x1 - masx[i]) * math.sin(a1) + (masy[i] - y1) * math.cos(a1)
            a_otn = math.atan2(Y, X)

            if dist < 5:
                break
            al1 = mB.position
            ar1 = mC.position
            a1 += math.radians((ar1 - ar2) - (al1 - al2)) * r / B
            x1 += math.cos(a1) * math.radians((ar1 - ar2) + (al1 - al2)) * r / 2
            y1 += math.sin(a1) * math.radians((ar1 - ar2) + (al1 - al2)) * r / 2

            Uv = kp1 * dist

            Up = kp2 * a_otn

            if Up > P:
                Up = P
            if Up < -P:
                Up = -P

            if Uv > V:
                Uv = V
            if Uv < -V:
                Uv = -V

            f.write(
                c + '=' + str(
                    al1) + ' ' + "ar1" + '=' + str(ar1) + ' ' + "Up" + '=' + str(Up) + ' ' + "Uv" + '=' + str(
                    Uv) + ' ' + str(a_otn*180/math.pi) + ' ' + str(i) + '\n')

            mB.run_direct(duty_cycle_sp=Uv - Up)
            mC.run_direct(duty_cycle_sp=Uv + Up)

            al2 = al1
            ar2 = ar1
print(str(v) + ' ' + str(w) + ' ' + str(p)+ ' ' + str(a))
finally:
    mB.stop(stop_action='brake')
    mC.stop(stop_action='brake')
    f.close