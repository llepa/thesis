from typing import overload
import matlab.engine
import time
import re
import matplotlib.pyplot as plt
import os
import numpy as np
import throttle
import json
import random

class SimulinkPlant:

    def __init__(self, jsonFile):
        f = open(jsonFile, 'r')
        self.inJ = json.load(f)
        self.modelName = self.inJ['modelName']
        self.modelPath = self.inJ['modelPath']
        self.noiseValues = self.inJ['noiseValues']
        self.outValues = self.inJ['outputValues']['values']
        self.outTS = self.inJ['outputValues']['time']
        self.out = dict()

    def setValue(self, varName, value):

        # Helper function to set value of control action
        # self.eng.set_param(self.handle, varName, str(value), nargout=0)
        self.eng.set_param(self.modelName + '/' + varName, 'Value', str(value), nargout=0)


    def getConstValue(self, value):
        return self.eng.get_param(self.modelName + '/' + value, 'Value')


    def getLastValue(self, value):
        return self.eng.eval(value)[-1]


    def getValue(self, value):

        # Helper function to get plant output and time 
        try:
            return self.eng.eval(value)
        except:
            print(value + ': Matlab type not supported in Python; converting...')
            #print(value)
            #print(type(value))
            return self.eng.eval('cast(vspeed.time, "int64")')


    def connectToMatlab(self):
        # Starting and connecting to Matlab
        print('Connecting...')
        print('Starting Matlab...')
        self.eng = matlab.engine.start_matlab()
        print('Connected to Matlab')

        # Loading the model
        print('Loading model...')

        self.eng.eval('model = "{}"'.format(self.modelPath), nargout=0)
        self.handle = self.eng.eval('load_system(model)')
        print('Model loaded')
        print('Connected')

    def intializeGraph(self):

        print('Initializing graph...')
        plt.close()
        plt.ion()
        for value in self.outValues:
            plt.plot(self.out[self.outTS], self.out[value], label=value)
            plt.legend()
        plt.title('test')
        plt.show()
        plt.pause(0.1)
        print('Graph initialized')


    def updateGraph(self):

        self.fig.set_xdata(self.out['tout'])
        self.fig.set_ydata(self.out['output'])
        #self.fig.set_ydata(self.out['simout'])

        plt.pause(0.1)
        plt.show()


    def print(self):
        graphString = ""
        legendString = ""
        for val in self.outValues:
            graphString += self.outTS + ','
            graphString += val + ','
            legendString += "\'" + val + "\',"
        printString = graphString[0: len(graphString)-1]
        legendString = legendString[0: len(legendString)-1]
        #self.eng.eval('f1 = figure')
        self.eng.eval('plot(' + printString + ')')
        self.eng.eval('legend({' + legendString + '})')
        #self.eng.eval('print("f1", "-djpeg")')


    def simulate(self, introduceError):

        t = 0.04             # the simulation stops 25 times per second
        sampleTime = 0.04    # second(s), chosen in [0.04, x], where x is the stop time of the simulation
        epsilon = 0.000000005
        self.eng.set_param(self.handle, 'SimulationCommand', 'start', 'SimulationCommand', 'pause', nargout=0)

        #print('Value of ' + 'throttle.signals.values' + 'before starting simulation: ' + str(self.getValue('throttle.signals.values')))

        if (introduceError):
            while (self.eng.get_param(self.handle, 'SimulationStatus') != ('stopped' or 'terminating')):     
                #print("Time: " + str(t))
                # OVVIAMENTE CORREGGERE QUESTO OBROBRIO QUI SOTTO !!!
                if (True):
                    for value in self.noiseValues:
                        #nominalVal = np.array(self.getLastValue(value[0]))[-1]
                        #nominalVal.astype(float)
                        r = random.random() - 0.5 
                        self.setValue(value[1], str(r))
                '''
                else:
                    for value in self.noiseValues:
                        self.setValue(value[1], str(0))
                '''
                t += 0.04
                self.eng.set_param(self.handle, 'SimulationCommand', 'continue', 'SimulationCommand', 'pause', nargout=0) 
        else:
            self.eng.set_param(self.handle, 'SimulationCommand', 'continue', nargout=0)

        '''
        self.out[self.outTS] = self.getValue(self.outTS)

        for value in self.outValues:
            self.out[value] = self.getValue(value)
        '''
        
        #self.intializeGraph()  
        self.print()

        s = ''
        while(s != 'y'):
            s = input('Do you want to finish the simulation? [y/n]: ')
        
        print('Simulation ended')


    def disconnect(self):
        print('Disconnecting...')
        self.eng.set_param(self.handle, 'SimulationCommand', 'stop', nargout=0)
        self.eng.quit()
        print('Disconnected')