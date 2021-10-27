import matlab.engine
import time
import os
import numpy as np
import markov
import json
import random

class SimulinkPlant:

    def __init__(self, json_file):
        f = open(json_file, 'r')
        self.in_j = json.load(f)
        self.models = self.in_j["models"]


    def extract_data(self, model):
        self.modelName = self.models[model]["modelName"]
        self.modelPath = self.models[model]["modelPath"]
        self.noiseValues = self.models[model]["noiseValues"]
        self.output = self.models[model]["output"]


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


    def disconnect(self):
        print('Disconnecting...')
        self.eng.set_param(self.handle, 'SimulationCommand', 'stop', nargout=0)
        self.eng.quit()
        print('Disconnected')


  # MODIFY THIS FUNCTION IN ORDER TO SET TO 0 THE ERROR WHEN introduceNoise IS SET TO False
    def initializeValues(self):
        for value in self.noiseValues:
            r = random.random()
            self.setValue(value[1], str(r))
        self.update()


    def update(self):
        self.eng.set_param(self.handle, 'SimulationCommand', 'update', nargout=0)


    def setValue(self, varName, value):
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
        

    def plot(self, plot_values, pos, n_plots):  
        graphString = ""
        legendString = ""
        for i in range(len(plot_values["values"])):
            graphString += plot_values["timestamps"][i] + ','
            graphString += plot_values["values"][i] + ','
            legendString += "\'" + plot_values["values"][i] + "\',"
        graphString = graphString[0: len(graphString)-1]
        legendString = legendString[0: len(legendString)-1]
        self.eng.eval('subplot(' + str(n_plots) + ',1,' + str(pos) + ')')
        self.eng.eval('plot(' + graphString + ')')
        self.eng.eval('legend({' + legendString + '})')


    def plotAll(self):
        self.eng.eval('figure')
        for i in range(len(self.output)):
            self.plot(self.output[i], i+1, len(self.output))


    def directSimulate(self):
        self.eng.eval('sim("' + self.modelName + '")', nargout=0)


    def simulate(self, introduceNoise):
        print('Starting simulation...')
        
        #t = 1                # the simulation stops _ times per second
        #sampleTime = 1         
        startTime = time.time()
        #self.eng.set_param(self.handle, 'SimulationCommand', 'start', 'SimulationCommand', 'pause', nargout=0)

        #self.initializeValues()

        if (introduceNoise):
            self.initializeValues()
            self.directSimulate()
            '''
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
                
                else:
                    for value in self.noiseValues:
                        self.setValue(value[1], str(0))
                
                t += 1
                self.eng.set_param(self.handle, 'SimulationCommand', 'continue', 'SimulationCommand', 'pause', nargout=0) 
                '''
        else:
            self.directSimulate()
               
        print("Simulation time: " + str(time.time() - startTime) + " seconds")

        '''
        if (introduceNoise):
            print("Number of steps taken: " + str(t))
            # DA RIVEDERE
            print("Sample time: " + str(12 / t))
        
        # interested simulation values are saved in a dictionary
        for i in range(len(self.output)):
            self.out[self.output]
        
        self.out[self.outTS] = self.getValue(self.outTS)

        for value in self.output:
            self.out[value] = self.getValue(value)
        '''

        self.plotAll()


    # first simulate the model without introducing noise, and then simulate it with noise 
    def fullSimulate(self):

        for b in [False, True]:
            self.simulate(b)
        s = ''
        while(s != 'y'):
            s = input('Do you want to end the simulation? [y/n]: ')
        

    def simulate_car(self):
        # extracts data needed to simulate the model
        self.extract_data(0)
        # load matlab and load the desired model 
        self.connectToMatlab()
        # run the simulation
        self.fullSimulate()
        # end the simulation, then the program
        self.disconnect()


    def simulate_apollo(self):
        # extracts data needed to simulate the model
        self.extract_data(1)
        # load matlab and load the desired model 
        self.connectToMatlab()
        # run the simulation
        self.fullSimulate()
        # end the simulation, then the program
        self.disconnect()
