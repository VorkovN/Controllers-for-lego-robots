#!/usr/bin/python3  
from ev3dev.ev3 import *  
import time
import math

mB = LargeMotor('outB')
mC = LargeMotor('outC')
us_sensor2 = UltrasonicSensor('in2')
us_sensor3 = UltrasonicSensor('in3')
f = open('lab4.txt','w')
f.write('0'+'0'+'\n')
start_time = time.time()
kp=30//для раст
ki=0.02//для раст
kd=40//для раст
kp2=100//для угла
kd2=200//для угла
h=175//раст между датчиками
dw=200//желаемое раст от стены
Uv=80//напряжение для движ прямо
o=30//где начинает копиться su
aw=10// max su
e_old=10//для раст
e_old2=0//для угла
su=0//нач инт сост
try:
    while True:
        d2 = us_sensor2.value()
        d3 = us_sensor3.value()
        e2=d3-d2//ошибка по углу
        dif2=e_old2-e2//диф сост для угла
        d=0.5*h*(d2+d3)*(1/math.sqrt(h*h+(d2-d3)*(d2-d3)))//стандартная формула раст
        e=(dw-d)//ошибка по раст
        su=su+e//инт сост для раст
        if abs(e)<o://ограничиваем раст на котором копится инт сост
            if abs(su+e)<aw://ограничиваем инт сост
                su=su+e//инт сост для раст
        dif=e-e_old//диф сост для раст
        Up=(kp*e+ki*su+kd*dif)+(kp2*e2+ki2*su2+kd2*dif2)//создаем напряжение для поворота
        e_old=e
        e_old2=e2
        if Up>20:
            Up=20
        if Up<-20:
            Up=-20
        mB.run_direct(duty_cycle_sp=Uv+Up)
        mC.run_direct(duty_cycle_sp=Uv-Up)
        current_time = time.time()-start_time
        if current_time > 15:
            break
        else:
            f.write(str(current_time)+ ' ' +str(d)+'\n')

finally:
    mB.stop(stop_action = 'brake')
    mC.stop(stop_action = 'brake')
    f.closeose