# Dies ist ein Testfile zum Testen der Kurvenfahrt mit Batterien
# Author: Urs Braun

# Imports
import move
import RPIservo
import time

# Konfig
robot_speed = 90
zeitfaktor = 1
lenkungsfaktor =1

#Object
scGear = RPIservo.ServoCtrl()

move.setup()
scGear.moveAngle(2, 0) # Lenker ausrichten

scGear.moveAngle(2, lenkungsfaktor*30)
move.move(robot_speed,'forward','no',0.9)
time.sleep(zeitfaktor*2.5) # Land 3

scGear.moveAngle(2, lenkungsfaktor*-30)
move.move(robot_speed, 'backward','left',0.9)
time.sleep(zeitfaktor*2.5)# Land 3

scGear.moveAngle(2, lenkungsfaktor*30)
move.move(robot_speed,'forward','no',0.9)
time.sleep(zeitfaktor*1.5) # Land 2

move.motorStop()
scGear.moveAngle(2, 10)