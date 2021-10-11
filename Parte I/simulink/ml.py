from typing import overload
import matlab.engine
import time
import re
import matplotlib.pyplot as plt
import os
import numpy as np
import markov
import json
import random

class SimulinkPlant:

    def __init__(self, jsonFile):
        f = open(jsonFile, 'r')
        self.inJ = json.load(f)
        m = 1
        self.models = self.inJ["models"]
        self.modelName = self.models[m]["modelName"]
        self.modelPath = self.models[m]["modelPath"]
        self.noiseValues = self.models[m]["noiseValues"]
        self.outValues = self.models[m]["outputValues"]["values"]
        self.outTS = self.models[m]["outputValues"]["time"]
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
            return self.eng.eval('cast(' + value + ', "double")')
        


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


    '''
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
    '''

    def plot(self):
        graphString = ""
        legendString = ""
        for val in self.outValues:
            graphString += self.outTS + ','
            graphString += val + ','
            legendString += "\'" + val + "\',"
        printString = graphString[0: len(graphString)-1]
        legendString = legendString[0: len(legendString)-1]
        self.eng.eval('plot(' + printString + ')')
        self.eng.eval('legend({' + legendString + '})')


    def fullSimulate(self):
        self.eng.eval('sim("' + self.modelName + '")', nargout=0)


    def initializeValues(self):
        for value in self.noiseValues:
            r = random.random() - 0.5
            self.setValue(value[1], str(r))

    def simulate(self, introduceError):
        print('Starting simulation...')
        
        t = 1                # the simulation stops _ times per second
        sampleTime = 1         
        startTime = time.time()
        #self.eng.set_param(self.handle, 'SimulationCommand', 'start', 'SimulationCommand', 'pause', nargout=0)

        self.initializeValues()
        
        if (introduceError):
            self.eng.set_param(self.handle, 'SimulationCommand', 'start', 'SimulationCommand', 'pause', nargout=0)
            #t += 1
            while (self.eng.get_param(self.handle, 'SimulationStatus') != ('stopped' or 'terminating')):     
                if (not t % sampleTime):
                    for value in self.noiseValues:
                        #nominalVal = np.array(self.getLastValue(value[0]))[-1]
                        #nominalVal.astype(float)
                        r = random.random() - 0.5     # based just on a random value but can be implemented in a more complex way
                        self.setValue(value[1], str(r))
                        self.eng.set_param(self.handle, 'SimulationCommand', 'update', nargout=0)
                '''
                else:
                    for value in self.noiseValues:
                        self.setValue(value[1], str(0))
                '''
                t += 1
                self.eng.set_param(self.handle, 'SimulationCommand', 'continue', 'SimulationCommand', 'pause', nargout=0) 
            #print(t)
        else:
            self.fullSimulate()
            
               
        
        print("Simulation time: " + str(time.time() - startTime) + " seconds")
        if (introduceError):
            print("Number of steps taken: " + str(t))
            print("Sample time: " + str(12 / t))
        
        
        # interested simulation values are saved in a dictionary
        self.out[self.outTS] = self.getValue(self.outTS)

        for value in self.outValues:
            self.out[value] = self.getValue(value)
        
        self.plot()

        s = ''
        while(s != 'y'):
            s = input('Do you want to end the simulation? [y/n]: ')
        
        print('Simulation ended')


    def disconnect(self):
        print('Disconnecting...')
        self.eng.set_param(self.handle, 'SimulationCommand', 'stop', nargout=0)
        self.eng.quit()
        print('Disconnected')