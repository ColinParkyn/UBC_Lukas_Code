#Set all channel defaults to be A for simplicity because we're only working with 1 channel

import comtypes.client as cc
from comtypes import COMError
import pyvisa as visa
cc.GetModule('Ke26XXA.dll')
import comtypes.gen.Ke26XXALib as Ke26XXALib
from ctypes import byref, pointer, c_long, c_float, c_int32, cast, c_char_p, c_char
from matplotlib.pyplot import plot,show
from numpy import arange,linspace
import time
class Ke26XXA(object):
    name = 'Keithley 26xxA'
        
    def __init__(self):
        self.inst = cc.CreateObject('Ke26XXA.Ke26XXA')
        
    def connect(self, visaAddr):
        self.inst.Initialize(visaAddr, False, False, '')
    
    # Sets the voltage for a channel. If cvMode is true sets channel automatically to constant voltage mode
    def setVoltage(self, v, chan='a',cvMode=True):
        if cvMode:
            self.setMode( 'cv')
        try:
            self.inst.Source.Voltage.Level[chan]=v
        except COMError:
            raise Ke26XXAException(self.checkError()[1])
        
    def getVoltage(self, chan='a'):
        try:
            res = self.inst.Measurement.Voltage.Measure(chan)
            #res = self.inst.Source.Voltage.Level[chan]          This is the old statement
        except COMError:
            raise Ke26XXAException(self.checkError()[1])
        return res
    
    # Sets the current for a channel. If ccMode is true sets channel automatically to constant current mode
    def setCurrent(self, c, chan='a',  ccMode=True):#renamed
        if ccMode:
            self.setMode( 'cc') 
        try:
            self.inst.Source.Current.Level[chan]=c        
        except COMError:
            raise Ke26XXAException(self.checkError()[1])
        
    def getCurrent(self, chan='a'):
        try:
            res = self.inst.Measurement.Current.Measure(chan)
        except COMError:
            raise Ke26XXAException(self.checkError()[1])
        return res
        
    def setVoltageAutorange(self, val,chan='a'):
        try:
            self.inst.Source.Voltage.AutoRangeEnabled[chan] = val
        except COMError:
            raise Ke26XXAException(self.checkError()[1])
        
    def setCurrentAutorange(self, val,chan='a'):
        try:
            self.inst.Source.Current.AutoRangeEnabled[chan] = val
        except COMError:
            raise Ke26XXAException(self.checkError()[1])
            
    def setCurrentMeasurementRange(self, val,chan='a'):
        try:
            self.inst.Measurement.Current.Range[chan] = val
        except COMError:
            raise Ke26XXAException(self.checkError()[1])
            
    def setVoltageLimit (self, val,chan='a'):
        try:
            self.inst.Source.Voltage.Limit[chan] = val
        except COMError:
            raise Ke26XXAException(self.checkError()[1])
            
    def setCurrentLimit(self, val, chan='a'):
        try:
            self.inst.Source.Current.Limit[chan] = val
        except COMError:
            raise Ke26XXAException(self.checkError()[1])

    # Sets mode to be constant current ('cc') or constant voltage ('cv')        
    def setMode(self, mode,chan='a'):
        # In COM driver, cc and cv are flipped
        modeDict = {'cv':1,\
                    'cc':0}
        try:
            self.inst.Source.Function[chan]=modeDict[mode]
        except COMError:
            raise Ke26XXAException(self.checkError()[1])
        except KeyError:
            raise Ke26XXAException('Mode must be either constant current (cc) or constant voltage (cv).')
     
    #set the auto zero function of the DAC  smua.AUTOZERO_OFF|smua.AUTOZERO_AUTO|smua.AUTOZERO_ONCE 
    def setAutoZeroMode(self, mode,chan='a'):
        # In COM driver, cc and cv are flipped
        modeDict = {'off':0,\
                    'once':1,\
                    'auto':2}
        try:
            self.inst.Measurement.AutoZero[chan]=modeDict[mode]
        except COMError:
            raise Ke26XXAException(self.checkError()[1])
        except KeyError:
            raise Ke26XXAException('Mode must be either off, once, or auto.')

    # Sets the integration time in number of power line cycles. Range 0.001 to 25 
    def setNPLC(self, val,chan='a'):
        try:
            self.inst.Measurement.NPLC[chan] = val
        except COMError:
            raise Ke26XXAException(self.checkError()[1])
    
    def outputenable(self, enable,chan='a'):
        try:
            self.inst.Source.OutputEnabled[chan] = enable
        except COMError:
            raise Ke26XXAException(self.checkError()[1])
    
    def checkError(self):        
        instErr, errMsg = self.inst.Utility.ErrorQuery()
        return instErr, errMsg
        
    def queryErrorStatus(self,val,chan='a'):
        self.inst.DriverOperation.QueryInstrumentStatus=val
        
    def set_sense_mode(self,sense_mode="remote"):
        if sense_mode == "remote":
            sense_mode = 1  # 1 or smuX.SENSE_REMOTE: Selects remote sense (4-wire)
        elif sense_mode == "local":
            sense_mode = 0  # 0 or smuX.SENSE_LOCAL: Selects local sense (2-wire)
        else:
            sense_mode = 0  # 0 or smuX.SENSE_LOCAL: Selects local sense (2-wire)
        self.write("{smuX}.sense = {sense_mode}".format(smuX=self.smu_full_string, sense_mode=sense_mode))


    def sweep(self,meas,actstar,actend,steps):#type in V and A, use string(For testing not used)
        start=actstar.split(" ")
        start=int(start[0])
        end=actend.split(" ")
        end=int(end[0])
        xran=linspace(start,end,steps)
        yran=[]
        if meas=="V":
            for i in range(steps):
                self.setCurrent(xran[i])
                yran.append(self.getVoltage())
        if meas=="C":
            for i in range(steps):
                self.setVoltage(xran[i])
                yran.append(self.getCurrent())
        print(xran,yran)
        plot(xran,yran)
        show()

class Ke26XXAException(Exception):
    pass