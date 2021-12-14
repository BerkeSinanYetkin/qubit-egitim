#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
import wpilib.drive
import ctre
from networktables import NetworkTables
import time
import logging
import math
from rev.color import ColorSensorV3




#### TIME.CLOCK
 

import logging

logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")

class MyRobot(wpilib.TimedRobot):



    def robotInit(self):
        self.weirdCounter = 0
        self.isBeltPerforming1 = False
        self.gyro = wpilib.ADXRS450_Gyro()
        self.isBeltPerforming2 = False
        self.left_encoder = wpilib.Encoder(0, 1)
        self.shooterRight = ctre.WPI_VictorSPX(5)
        self.shooterLeft = ctre.WPI_VictorSPX(6)
        self.shooterRight.setSafetyEnabled(False)
        self.shooterLeft.setSafetyEnabled(False)


        wpilib.CameraServer.launch()

        self.allowed = True

        self.beltMotor = ctre.WPI_VictorSPX(9)
        self.beltMotor.setSafetyEnabled(False)

        self.intakeRedline = ctre.WPI_VictorSPX(8)
        self.hopper = ctre.WPI_VictorSPX(7)
        self.intakeRedline.setSafetyEnabled(False)
        self.hopper.setSafetyEnabled(False)

        #self.lightSel = wpilib.Solenoid()
        self.gyroCounter = 0
        self.alreadyDone = False

        self.canBusSPX1 = ctre.WPI_VictorSPX(1)
        self.canBusSPX2 = ctre.WPI_VictorSPX(2)
        self.canBusSPX3 = ctre.WPI_VictorSPX(3)
        self.canBusSPX4 = ctre.WPI_VictorSPX(4)
        self.canBusSPX1.setSafetyEnabled(False)
        self.canBusSPX2.setSafetyEnabled(False)
        self.canBusSPX3.setSafetyEnabled(False)
        self.canBusSPX4.setSafetyEnabled(False)




        self.isHopperWorking = False




        self.shootCounter = 0
        self.intakeCounter = 0


        self.didres = False

        self.isStored = False
        self.storedData = 0

        self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)

        self.kompresor = wpilib.Compressor(0)

        self.intakeSel = wpilib.DoubleSolenoid(0, 2, 3)  #intake
        self.shooterSel = wpilib.DoubleSolenoid(0, 0, 1) #shooter
        self.climbingSel1 = wpilib.DoubleSolenoid(0, 4, 5)
        self.climbingSel2 = wpilib.DoubleSolenoid(0, 6, 7)

        self.fireCounter = False

        self.kompresor.setClosedLoopControl(True)
        self.kompresor.start()
        self.currentlyWorking = False

        self.count = 0

        self.drive = wpilib.drive.DifferentialDrive(self.canBusSPX2, self.canBusSPX4)
        self.drive2 = wpilib.drive.DifferentialDrive(self.canBusSPX1, self.canBusSPX3)

        self.stick = wpilib.Joystick(0)

        self.stick2 = wpilib.Joystick(1)

        self.coooounter = 0

        self.timer = wpilib.Timer()

        self.gyro.calibrate()



    def autonomousInit(self):
        
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        

        if self.timer.get() < 1.5:
            self.drive.arcadeDrive(0.6, 0)  # fwd, rot
            self.drive2.arcadeDrive(0.6, 0)  # fwd, rot
        else:
            self.drive.arcadeDrive(0, 0)  
            self.drive2.arcadeDrive(0, 0)


    def intakeAll(self):
        if self.shouldWork() == True:
            self.shooterRight.set(0.75)
            self.shooterLeft.set(-0.75)
            self.hopper.set(-1)
            self.intakeRedline.set(0.45)
            self.intakeSel.set(wpilib.DoubleSolenoid.Value.kReverse)
            self.shooterSel.set(wpilib.DoubleSolenoid.Value.kReverse)
            
        else:
            self.isBeltPerforming1 = True
            self.shooterRight.set(0.75) #############
            self.shooterLeft.set(-0.75) #############
            self.hopper.set(-1) #############
            self.intakeRedline.set(0.4) #############
            self.intakeSel.set(wpilib.DoubleSolenoid.Value.kReverse)
            self.beltMotor.set(1)
            #self.hopper.set(-0.5)
            time.sleep(3)
            self.beltMotor.set(0)
            #self.hopper.set(0)


    def handleN(self):
        if self.allowed == True:
            self.intakeSel.set(wpilib.DoubleSolenoid.Value.kForward)
            self.shooterSel.set(wpilib.DoubleSolenoid.Value.kReverse)
            sd.putString("SEL PROCESS", "YES")
            
            if self.alreadyDone == False:
                sd.putString("Worked By Already done", "YES")
                self.drive.arcadeDrive(1, 0)  # fwd, rot
                self.drive2.arcadeDrive(1, 0)  # fwd, rot
                time.sleep(1)
                self.drive.arcadeDrive(0, 0)  # fwd, rot
                self.drive2.arcadeDrive(0, 0)  # fwd, rot
                self.alreadyDone = True
                self.fire()
                print("fired")
            else:      
                
                print("arcade things")


   
    def handleRed(movementForX, movementForY):

        if movementForY != "center" and movementForX != "center":
            self.shooterRight.set(0)
            self.shooterLeft.set(0)
            # self.hopper.set(0)
            self.beltMotor.set(0)
            self.isBeltPerforming2 = False

        if movementForY != "center":
            if movementForY == "upper":
                self.drive.arcadeDrive(1, 0)  # fwd, rot
                self.drive2.arcadeDrive(1, 0)  # fwd, rot
                time.sleep(0.3)
            elif movementForY == "lower":
                self.drive.arcadeDrive(-1, 0)  # fwd, rot
                self.drive2.arcadeDrive(-1, 0)  # fwd, rot
                time.sleep(0.3)
        else:
            if movementForX != "center":
                if movementForX == "right":
                    self.drive.arcadeDrive(0, 1)  # fwd, rot
                    self.drive2.arcadeDrive(0, 1)  # fwd, rot
                    time.sleep(0.3)
                elif movementForX == "left":
                    self.drive.arcadeDrive(0, -1)  # fwd, rot
                    self.drive2.arcadeDrive(0, -1)  # fwd, rot
                    time.sleep(0.3)
            else:
                self.fire()

    def addFireItems(self):
        sd.putString("fire started", "NO")
        sd.putString("Did get started by time get 10", "NO")
        sd.putString("fire killed", "NO")

    
    def fire(self):
        sd.putString("fire started", "YES")
        if self.fireCounter == False:
            print("h") ####
            self.fireCounter = True

        while True:


            sd.putString("Did get started by time get 10", "YES")
            if True: ####hasto be false
                self.shooterRight.set(-0.60)
                self.shooterLeft.set(0.60)
                self.shooterSel.set(wpilib.DoubleSolenoid.Value.kReverse)
                if self.isHopperWorking == False:
                    time.sleep(3)
                    self.hopper.set(1)
                    self.isHopperWorking = True
                    self.beltMotor.set(0)
            else:
                self.beltMotor.set(-1)
                self.isBeltPerforming2 = True
                # self.hopper.set(1)
        else:
            self.fireCounter = False
            self.alreadyDone = True
            sd.putString("fire killed", "YES")


    def getColor(self):
        return self.colorSensor.getColor()

    def shouldWork(self):
        colooooor = self.getColor()
        BBool = False

       



      

        if colooooor.red > 0.28 and  0.34 >colooooor.red and colooooor.blue > 0.09 and  0.18 >colooooor.blue and colooooor.green > 0.53 and  0.58 > colooooor.green:
            sd.putString("Color Tracking", "YES")
            return False
        else:
            sd.putString("Color Tracking", "NO")
            return True


    def possibleRefXStatusFormatter(refXCoordinate):
        status = ""
        try:
            if refXCoordinate > 0:
                if refXCoordinate > 280 and refXCoordinate < 380:
                    status = "center"
                elif 280 > refXCoordinate:
                    status = "right"
                elif refXCoordinate > 380:
                    status = "left"
                return status
        except:
            return "null"

    def possibleRefYStatusFormatter(refYCoordinate):
        status = ""
        try:
            if refXCoordinate > 0:
                if refXCoordinate > 150 and refXCoordinate < 250:
                    status = "center"
                elif 150 > refXCoordinate:
                    status = "upper"
                elif refXCoordinate > 250:
                    status = "lower"
                return status
        except:
            return "null"

    def gyroAD(self):
        self.gyroCounter += 1
        self.angle = self.gyro.getAngle()
        print("this")
        print("this")
        print("this")
        print("this")
        print("this")
        print("this")
        print("this")
        print("this")
        print("this")
        print("this")

        if 500 < self.gyroCounter and self.currentlyWorking == False:
            return
            self.gyro.calibrate()

        if self.angle < -3:
            self.drive.arcadeDrive(self.stick.getY() * 0.75, 0.5)  # fwd, rot
            self.drive2.arcadeDrive(self.stick.getY() * 0.75, 0.5)  # fwd, rot
        elif 3 < self.angle:
            self.drive.arcadeDrive(self.stick.getY() * 0.75, -0.5)  # fwd, rot
            self.drive2.arcadeDrive(self.stick.getY() * 0.75, -0.5)  # fwd, rot
        # self.drive2.arcadeDrive(self.stick.getY(), self.turningValue)
        # self.drive.arcadeDrive(self.stick.getY(), self.turningValue)


    def teleopPeriodic(self):        

        self.kompresor.start()
        #result = sd.getString("balllcX", "aaa")
        if self.currentlyWorking == False:
            self.drive.arcadeDrive(self.stick.getY()*0.75, self.stick.getZ()*0.75)#fwd, rot
            self.drive2.arcadeDrive(self.stick.getY()*0.75, self.stick.getZ()*0.75)#fwd, rot

        if self.stick2.getRawButton(3) and self.coooounter == 0:
            self.shooterRight.set(0.7)
            self.shooterLeft.set(-0.7)
        elif self.stick2.getRawButton(4) and self.coooounter == 0:
            self.shooterRight.set(-0.7)
            self.shooterLeft.set(0.7)
        elif self.stick2.getRawButton(1) == False and self.stick2.getRawButton(2) == False:
            self.shooterRight.set(0)
            self.shooterLeft.set(0)


############intake
        if self.stick2.getRawButton(10):  #INTAKE SEL
            self.intakeSel.set(wpilib.DoubleSolenoid.Value.kForward)
        elif self.stick2.getRawButton(9):
            self.intakeSel.set(wpilib.DoubleSolenoid.Value.kReverse)
        elif self.stick2.getRawButton(2)== False and self.stick2.getRawButton(5) == False and self.stick2.getRawButton(6) == False:
            self.intakeSel.set(wpilib.DoubleSolenoid.Value.kOff)
#8




        if self.shouldWork():
            sd.putString("ballB", "NO")
        else:
            sd.putString("ballB", "YES")


        cooooloer = self.colorSensor.getColor()
        sd.putString("red", str(cooooloer.red))
        sd.putString("blue", str(cooooloer.blue))
        sd.putString("green", str(cooooloer.green))

        if self.stick2.getRawButton(12):
            self.shooterSel.set(wpilib.DoubleSolenoid.Value.kReverse)
        elif self.stick2.getRawButton(11):
            self.shooterSel.set(wpilib.DoubleSolenoid.Value.kForward)
        elif self.stick2.getRawButton(1) == False and self.stick2.getRawButton(2) == False:
            self.shooterSel.set(wpilib.DoubleSolenoid.Value.kOff)

# 8-9



        if self.stick2.getRawButton(5):
            self.climbingSel1.set(wpilib.DoubleSolenoid.Value.kForward)
            self.climbingSel2.set(wpilib.DoubleSolenoid.Value.kForward)
        elif self.stick2.getRawButton(6):
            self.climbingSel1.set(wpilib.DoubleSolenoid.Value.kReverse)
            self.climbingSel2.set(wpilib.DoubleSolenoid.Value.kReverse)
        else:
            self.climbingSel1.set(wpilib.DoubleSolenoid.Value.kOff)
            self.climbingSel2.set(wpilib.DoubleSolenoid.Value.kOff)
            #self.intakeSel.set(wpilib.DoubleSolenoid.Value.kOff)

          ########################################################################################

################################################################   HOPPER ATMA
        if self.stick2.getRawButton(8):
            self.hopper.set(1)
        elif self.stick2.getRawButton(7):
            self.hopper.set(-1)
        else:
            self.hopper.set(0)
################################################################   HOPPER ATMA
################################################################   TOP ATMA
        if self.stick2.getRawButton(1):

            if self.shouldWork() == False:
                self.shooterRight.set(-0.60)
                self.shooterLeft.set(0.60)
                self.shooterSel.set(wpilib.DoubleSolenoid.Value.kReverse)
                time.sleep(3)
                #self.hopper.set(1)
                self.beltMotor.set(0)
            else:
                self.beltMotor.set(-1)
                self.isBeltPerforming2 = True
                self.shooterSel.set(wpilib.DoubleSolenoid.Value.kReverse)

            #self.hopper.set(1)
        elif self.stick2.getRawButton(8) == False and self.stick2.getRawButton(7) == False and self.stick2.getRawButton(4) == False and self.stick2.getRawButton(3) == False and self.stick2.getRawButton(1) == False and self.stick2.getRawButton(2) == False and self.stick2.getRawButton(10) == False:
            self.shooterRight.set(0)
            self.shooterLeft.set(0)
            #self.hopper.set(0)
            self.beltMotor.set(0)
            self.isBeltPerforming2 = False
################################################################   TOP ATMA
        
        if self.stick.getRawButton(9):
            self.intakeRedline.set(-0.5)
        elif self.stick.getRawButton(8):
            self.intakeRedline.set(0.5)
        
################################################################   TOP ALMA
        if self.stick2.getRawButton(2):
            if self.shouldWork() == True:
                self.shooterRight.set(0.60)
                self.shooterLeft.set(-0.60)
                self.hopper.set(-0.7)
                self.intakeRedline.set(0.45)
                self.intakeSel.set(wpilib.DoubleSolenoid.Value.kReverse)
                self.shooterSel.set(wpilib.DoubleSolenoid.Value.kForward)
                
            else:
                self.isBeltPerforming1 = True
                self.shooterRight.set(0.60) #############
                self.shooterLeft.set(-0.60) #############
                self.hopper.set(-0.7) #############
                self.intakeRedline.set(0.4) #############
                self.intakeSel.set(wpilib.DoubleSolenoid.Value.kReverse)
                self.beltMotor.set(1)
                #self.hopper.set(-0.5)
                time.sleep(2)
                self.beltMotor.set(0)
                #self.hopper.set(0)
        elif self.stick2.getRawButton(7) == False and self.stick.getRawButton(9) == False and self.stick.getRawButton(8) == False and self.stick2.getRawButton(9) == False and self.stick2.getRawButton(8) == False and self.stick.getRawButton(4) == False and self.stick.getRawButton(3) == False and self.stick2.getRawButton(1) == False and self.stick2.getRawButton(4) == False and self.stick2.getRawButton(3)  == False and self.stick2.getRawButton(1) == False and self.stick2.getRawButton(8) == False and self.stick2.getRawButton(2) == False and self.stick2.getRawButton(10) == False:
            self.shooterRight.set(0)
            self.isBeltPerforming1 = False
            self.shooterLeft.set(0)
            self.hopper.set(0)
            self.intakeRedline.set(0)
            self.intakeSel.set(wpilib.DoubleSolenoid.Value.kOff)  #############

        ################################################################   TOP ALMA






        if self.isBeltPerforming1 == False and self.isBeltPerforming2 == False:
            if self.stick2.getY() > 0.5 or -0.5 > self.stick2.getY():
                self.beltMotor.set(self.stick2.getY())
            else:
                self.beltMotor.set(0)



        if self.stick.getRawButton(8):

            if self.weirdCounter == 0:
                self.weirdCounter += 1
            if self.weirdCounter == 1:
                self.gyro.calibrate()
                self.weirdCounter += 1

            self.gyroAD()
            self.currentlyWorking = True
        else:
            self.currentlyWorking = False
            self.weirdCounter = 0

        sd.putString("gyroAngle", str(self.gyro.getAngle()))



if __name__ == "__main__":
    wpilib.run(MyRobot)
