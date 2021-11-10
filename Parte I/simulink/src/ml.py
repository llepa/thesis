import matlab.engine
import time
import os
import numpy as np
import markov
import json
import random
import sys
import pandas as pd
import statsmodels.stats.weightstats as ws
import my_stats

class SimulinkPlant:

    def __init__(self, json_file):
        f = open(json_file, 'r')
        self.in_j = json.load(f)
        self.models = self.in_j["models"]
        self.base_path = os.getcwd()
        self.connected = False
        

    def extract_simulation_data(self, model):
        self.model_name = self.models[model]["model_name"]
        self.model_path = self.models[model]["model_path"]
        self.output = self.models[model]["output"]
        self.csv = self.models[model]["csv"]
        self.noisy_csv = self.models[model]["noisy_csv"]
        self.stats_csv = self.models[model]["stats_csv"]
        self.noisy_stats_csv = self.models[model]["noisy_stats_csv"]
        self.model_directory = self.models[model]["model_directory"]
        self.data_directory = self.models[model]["data_directory"]
        self.var = self.models[model]["variance"]


    def create_data_structures(self):

        self.names = list()
        for d in self.output:
            self.names += d["names"]
        self.csv_data = pd.DataFrame(columns=self.names)
        self.csv_data.reset_index(drop=True, inplace=True)

        cols = ["values", "mean", "variance"]
        self.csv_stats = pd.DataFrame(columns=cols)
        self.csv_stats['values'] = self.names
        self.csv_stats.set_index('values', inplace=True)


    def connect_to_Matlab(self):
        # Starting and connecting to Matlab
        print('Connecting...')
        print('Starting Matlab...')
        self.eng = matlab.engine.start_matlab()
        print('Connected to Matlab')

        # Loading the model
        print('Loading model...')
        self.eng.eval('model = "{}"'.format(self.model_name), nargout=0)
        self.handle = self.eng.eval('load_system(model)')
        self.connected = True
        print('Model loaded')
        print('Connected')


    def disconnect(self):
        print('Disconnecting...')
        # self.eng.set_param(self.handle, 'SimulationCommand', 'stop', nargout=0)
        self.eng.quit()
        print('Disconnected')

    
    # MAYBE TO BE DELETED
    def initializeValues(self):
        for value in self.noiseValues:
            r = random.random()
            self.set_value(value[1], str(r))
        self.update()


    def update(self):
        self.eng.set_param(self.handle, 'SimulationCommand', 'update', nargout=0)


    def set_value(self, varName, value):
        # self.eng.set_param(self.handle, varName, str(value), nargout=0)
        self.eng.set_param(self.model_name + '/' + varName, 'Value', str(value), nargout=0)


    # MAYBE TO BE DELETED
    def getConstValue(self, value):
        return self.eng.get_param(self.model_name + '/' + value, 'Value')

    
    # MAYBE TO BE DELETED
    def getLastValue(self, value):
        return self.eng.eval(value)[-1]


    def get_value(self, value):
        # Helper function to get plant output and time 
        try:
            # return self.eng.eval(value)
            return self.eng.workspace[value]
        except:
            print(value + ': Matlab type not supported in Python; converting...')
            #print(value)
            #print(type(value))
            return self.eng.eval('cast(' + value + ', "double")')
        
    
    def set_var(self):
        for el in self.var:
            self.set_value(el[0], str(el[1]))

        
    def plot(self, plot_values, pos, n_plots):  
        graphString = ""
        legendString = ""
        for i in range(len(plot_values["values"])):
            # print(plot_values["values"])
            # graphString += plot_values["timestamps"][i] + ','
            length = len(self.csv_data[plot_values["names"][i]])
            graphString += "1:" + str(length) + ','
            graphString += plot_values["values"][i] + ','
            legendString += "\'" + plot_values["names"][i] + "\',"
        graphString = graphString[0: len(graphString)-1]
        legendString = legendString[0: len(legendString)-1]
        self.eng.eval('subplot(' + str(n_plots) + ',1,' + str(pos) + ')')
        self.eng.eval('plot(' + graphString + ')')
        self.eng.eval('legend({' + legendString + '})')


    def plotAll(self):
        self.eng.eval('figure')
        for i in range(len(self.output)):
            self.plot(self.output[i], i+1, len(self.output))

        s = ''
        while(s != 'y'):
            s = input('Do you want to end the simulation? [y/n]: ')


    def directSimulate(self):
        return self.eng.sim(self.model_name)


    def write_helper(self, l):
        return [v[0] for v in l]


    def simulate(self):
        print('Starting simulation...')
        startTime = time.time()

        self.directSimulate()
        #self.eng.set_param(self.model_name, 'SimulationCommand', 'WriteDataLogs', nargout=0);

        print("Simulation time: " + str(time.time() - startTime) + " seconds")

        # self.out[self.outTS] = self.get_value(self.outTS)


    def calculate_stats(self):
        self.csv_stats['mean'] = my_stats.iter(self.csv_data, 1)
        self.csv_stats['variance'] = my_stats.citer(self.csv_data, 2)
        print(self.csv_stats)


    def extract_data(self):
        for out in self.output:
            for i in range(len(out["values"])):
                name = out["names"][i]
                value = self.get_value(out["values"][i])
                self.csv_data[name] = self.write_helper(value)
                # print(value)
                # self.csv_data[self.names[i]] = pd.Series(self.get_value(self.output[i]))


    def write_data(self):
        os.chdir(self.data_directory)

        if (self.noisy):   
            self.csv_data.to_csv(self.noisy_csv, index=False)
        else:
            self.csv_data.to_csv(self.csv, index=False)

        os.chdir(self.base_path)


    def write_stats(self):
        os.chdir(self.data_directory)

        if (self.noisy):
            self.csv_stats.to_csv(self.noisy_stats_csv)
        else:
            self.csv_stats.to_csv(self.stats_csv)
        
        os.chdir(self.base_path)
    

    def simulate_car(self, noisy):

        # extracts data needed to simulate the model
        self.extract_simulation_data(0)

        os.chdir(self.model_directory)

        # load matlab and load the desired model 
        if (not self.connected):
            self.connect_to_Matlab()
        
        if (noisy):
            self.noisy = True
            self.set_var()
        else:
            self.noisy = False

        # run the simulation
        self.simulate()

        os.chdir(self.base_path)

        # create data structures for model data and stats storage
        self.create_data_structures()

        # extract data from model and save it in csv format file
        self.extract_data()
        self.write_data()

        # plot values
        self.plotAll()

        # calculate stats and save it in csv format file
        self.calculate_stats()
        self.write_stats()
        
        # print("Correlation:")
        # print(self.corr(self.csv_data))
        
        # end the simulation, then the program
        self.disconnect()


    def simulate_apollo(self, noisy):
        # extracts data needed to simulate the model
        self.extract_simulation_data(1)
        
        # load matlab and load the desired model 
        self.connect_to_Matlab()
        

        # end the simulation, then the program
        self.disconnect()

sm = SimulinkPlant('input.json')
sm.simulate_car(False)