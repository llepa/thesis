import matlab.engine
import time
import re
import matplotlib.pyplot as plt
import os
import numpy as np
import throttle

class SimulinkPlant:

    def __init__(self, modelName, outValues, timestamps):
        self.modelName = modelName
        self.out = dict()
        self.outValues = outValues
        self.outTs = timestamps


    def setValue(self, varName, value):

        # Helper function to set value of control action
        # self.eng.set_param(self.handle, varName, str(value), nargout=0)
        self.eng.workspace[varName] = value


    def connectToMatlab(self):

        # Starting and connecting to Matlab
        print('Connecting...')
        print('Starting Matlab...')
        self.eng = matlab.engine.start_matlab()
        print('Connected to Matlab')

        # Loading the model
        print('Loading model...')

        self.eng.eval('model = "{}"'.format(self.modelName), nargout=0)
        self.handle = self.eng.eval('load_system(model)')

        print('Model loaded')
        print('Connected')


    def getValue(self, value):

        # Helper function to get plant output and time 
        try:
            return self.eng.eval(value)
        except:
            print('Matlab type not supported in Python; converting...')
            print(value)
            print(type(value))
            return self.eng.eval('cast(vspeed.time, "int64")')


    def intializeGraph(self):

        print('Initializing graph...')
        plt.close()
        plt.ion()
        for value in self.outValues:
            r = np.random.randint(256)
            g = np.random.randint(256)
            b = np.random.randint(256)
            plt.plot(self.outTs, self.out[value], label=value)
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

        '''
        while (self.eng.get_param(self.modelName, 'SimulationStatus') != ('stopped' or 'terminating')):
            self.eng.set_param(self.modelName, 'SimulationCommand', 'continue', 'SimulationCommand', 'pause', nargout=0)
        '''

        i = ''
        while(i != 'y'):
               
            print('Initializing variable: sigin')

            t = throttle.ThrottleMarkov(5, 100, 50)
            print(t.getValues())
            self.setValue('sigin', matlab.double(t.getValues()))
       
            print('Variable sigin initialized')

            # Start simulation
            print('Starting simulation...') 

            self.eng.set_param(self.handle, 'SimulationCommand', 'start', nargout=0)

            self.outTs = self.getValue(self.outTs)

            for value in self.outValues:
                self.out[value] = self.getValue(value)
            
            self.intializeGraph()    
        
            print('Simulation ended')

            i = input("Do you want to stop? [y/n]: ") 

    def disconnect(self):
        print('Disconnecting...')
        self.eng.set_param(self.handle, 'SimulationCommand', 'stop', nargout=0)
        self.eng.quit()
        print('Disconnected')