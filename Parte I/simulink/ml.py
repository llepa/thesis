import matlab.engine
import time
import re
import matplotlib.pyplot as plt
import os
import numpy as np
import throttle

class SimulinkPlant:

    def __init__(self, modelName, modelPath, outValues, timestamps):
        self.modelName = modelName
        self.modelPath = modelPath
        self.out = dict()
        self.outValues = outValues
        self.outTS = timestamps
        

    def setValue(self, varName, value):

        # Helper function to set value of control action
        # self.eng.set_param(self.handle, varName, str(value), nargout=0)
        self.eng.set_param(self.modelName + '/' + varName, 'Value', str(value), nargout=0)

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

        self.eng.set_param(self.handle, 'SimulationCommand', 'start', 'SimulationCommand', 'pause', nargout=0)

        print('Model loaded')
        print('Connected')


    def getValue(self, value):

        # Helper function to get plant output and time 
        try:
            return self.eng.eval(value)
        except:
            print(value + ': Matlab type not supported in Python; converting...')
            #print(value)
            #print(type(value))
            return self.eng.eval('cast(vspeed.time, "int64")')


    def intializeGraph(self):

        print('Initializing graph...')
        plt.close()
        plt.ion()
        for value in self.outValues:
            r = np.random.randint(256)
            g = np.random.randint(256)
            b = np.random.randint(256)
            plt.plot(self.outTS, self.out[value], label=value)
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


    def simulate(self):

        t = 1           # the simulation stops 25 times per second
        sampleTime = 1  # second(s), chosen in [0.04, x], where x is the stop time of the simulation

        while (self.eng.get_param(self.handle, 'SimulationStatus') != ('stopped' or 'terminating')):
            
            '''
            print('Initializing variable: sigin')    
            
            print(t.getValues())
            self.setValue('sigin', matlab.double(t.getValues()))
            print('Variable sigin initialized')
            '''
            #t = throttle.ThrottleMarkov(5, 100, 50)

            #if (not (t / 25) % sampleTime):
                # thr = self.getValue('throttle')
                
            self.setValue('throttleNoise', 100)
            self.eng.set_param(self.handle, 'SimulationCommand', 'continue', 'SimulationCommand', 'pause', nargout=0)

            t += 1

        self.outTS = self.getValue(self.outTS)

        for value in self.outValues:
            self.out[value] = self.getValue(value)

        self.intializeGraph()  

        s = ''
        while(s != 'y'):
            s = input('Do you want to finish the simulation? [y/n]: ')

        print('Simulation ended')


    def disconnect(self):
        print('Disconnecting...')
        self.eng.set_param(self.handle, 'SimulationCommand', 'stop', nargout=0)
        self.eng.quit()
        print('Disconnected')