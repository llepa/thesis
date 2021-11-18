import matlab.engine
import time
import os
import numpy as np
import json
import random
import pandas as pd
import statsmodels.stats.weightstats as ws
import my_stats
import statsmodels.stats.descriptivestats as ds
import math
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
import warnings
from sklearn.model_selection import ShuffleSplit, cross_val_score



# DECIDERE BENE QUESTI PARAMETRI
SIMULATION_TIME = 1800
READINGS_PER_SECOND = 25
TOTAL_READINGS = SIMULATION_TIME * READINGS_PER_SECOND
CHUNK_SIZE_CAR = 25
CHUNK_SIZE_APOLLO = 0

class SimulinkPlant:

    def __init__(self, json_file):
        f = open(json_file, 'r')
        self.in_j = json.load(f)
        self.models = self.in_j["models"]
        self.base_path = os.getcwd()
        self.connected = False
        self.DB = {}
        warnings.simplefilter(action='ignore', category=FutureWarning)
        

    def extract_simulation_data(self, model):
        self.model = model
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
        self.variance_tuples = self.models[model]["variance_tuples"]
        self.residual_csv = self.models[model]["residual_csv"]
        self.sensor_ID = self.models[model]["sensor_ID"]
        

    def create_data_structures(self):

        self.sensor_name = list()
        self.residual_name = list()
        for d in self.output:
            self.sensor_name += d["values"]
            for r in d["residual"]:
                self.residual_name.append(r[0])
        self.csv_data = pd.DataFrame(columns=self.sensor_name)
        self.csv_data.reset_index(drop=True, inplace=True)
        self.residual_df = pd.DataFrame(columns=self.residual_name)
        self.residual_df.reset_index(drop=True, inplace=True)

        cols = ["sensor_residual", "mean", "variance", "std_dev", "skewness", "kurtosis"]
        self.residual_stats = pd.DataFrame(columns=cols)
        self.residual_stats['sensor_residual'] = self.residual_name
        self.residual_stats.set_index('sensor_residual', inplace=True)


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
    def get_constant_value(self, value):
        return self.eng.get_param(self.model_name + '/' + value, 'Value')

    
    # MAYBE TO BE DELETED
    def get_last_value(self, value):
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
        

    def set_spec_var(self, name, value):
         self.set_value(name, str(value))

        
    def plot(self, plot_values, pos, n_plots):  
        graphString = ""
        legendString = ""
        for i in range(len(plot_values["plot"])):
            # print(plot_values["values"])
            # graphString += plot_values["timestamps"][i] + ','
            length = len(self.csv_data[plot_values["plot"][i]])
            graphString += "1:" + str(length) + ','
            graphString += plot_values["plot"][i] + ','
            legendString += "\'" + plot_values["plot"][i] + "\',"
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

        print("Simulation ended in " + str(time.time() - startTime) + " seconds")

        # self.out[self.outTS] = self.get_value(self.outTS)


    def residual_residual_stats(self, vector):
        stats1 = ws.DescrStatsW(vector)
        stats2 = ds.describe(vector)

        # self.residual_stats['mean'] = my_stats.iter(self.csv_data, 1)
        # self.residual_stats['variance'] = my_stats.citer(self.csv_data, 2)
        # "mean", "variance", "std_dev", "skewness", "kurtosis"
        self.residual_stats['mean'] = stats1.mean
        self.residual_stats['variance'] = stats1.var
        self.residual_stats['std_dev'] = stats1.std
        self.residual_stats['skewness'] = stats2.skew()
        self.residual_stats['kurtosis'] = stats2.kurtosis()
        print(self.residual_stats)
        print()


    def compute_residual(self, r1, r2):
        return r1.subtract(r2, fill_value=0)


    def extract_data(self):
        for out in self.output:
            for i in range(len(out["values"])):
                name = out["values"][i]
                value = self.get_value(name)
                self.csv_data[name] = self.write_helper(value)
                # print(value)
                # self.csv_data[self.sensor_name[i]] = pd.Series(self.get_value(self.output[i]))
            
            for i in range(len(out["residual"])):
                residual = out["residual"][i]
                value = self.compute_residual(self.csv_data[residual[1]], self.csv_data[residual[2]])
                self.residual_df[residual[0]] = value


    def write_data(self):
        os.chdir(self.data_directory)

        # if (self.noisy):   
        #     self.csv_data.to_csv(self.noisy_csv, index=False)
        # else:
        #     self.csv_data.to_csv(self.csv, index=False)

        self.csv_data.to_csv(self.csv, index=False)
        self.residual_df.to_csv(self.residual_csv, index=False)
        os.chdir(self.base_path)


    def write_stats(self):
        os.chdir(self.data_directory)

        # if (self.noisy):
        #     self.residual_stats.to_csv(self.noisy_stats_csv)
        # else:
        #     self.residual_stats.to_csv(self.stats_csv)
        
        self.residual_stats.to_csv(self.stats_csv)
        os.chdir(self.base_path)


    def add_feature(self, chunk, sensor):
        
        stats1 = ws.DescrStatsW(chunk)
        stats2 = ds.describe(chunk)

        data = []
        data.append(stats1.mean)
        data.append(stats1.var)
        data.append(stats1.std)
        data.append(stats2.skew()[sensor])
        data.append(stats2.kurtosis()[sensor])     
        
        return data


    def split_residuals(self, size=0, seek=False):
        print("Splitting residuals...")
        i = 0
        X_temp = []
        y_temp = []
        target_list = []

        if (seek == True):
            chunk_size = size
        else:
            if (self.model == 0):
                chunk_size = CHUNK_SIZE_CAR
            elif (self.model == 1):
                chunk_size = CHUNK_SIZE_APOLLO
        
        print("Chunk size: " + str(chunk_size))

        for sensor in self.residual_df.columns:
            target_list.append(sensor)
            while (i < len(self.residual_df[sensor])):
                if (i + 2 * chunk_size > len(self.residual_df[sensor])):
                    X_temp.append(self.add_feature(self.residual_df[sensor][i: i+chunk_size], sensor))
                    y_temp.append(self.sensor_ID[sensor])
                    i += chunk_size * 2
                else:
                    if (i + chunk_size > len(self.residual_df[sensor])):
                        X_temp.append(self.add_feature(self.residual_df[sensor][i:], sensor))
                        y_temp.append(self.sensor_ID[sensor])
                    else:
                        X_temp.append(self.add_feature(self.residual_df[sensor][i: i+chunk_size], sensor))
                        y_temp.append(self.sensor_ID[sensor])
                    i += chunk_size
            i = 0
        
        self.DB['data'] = np.array(X_temp)
        self.DB['target'] = np.array(y_temp)
        self.DB['target_names'] = np.array(target_list)
        
        print(self.DB)
        print("Residual splitted")


    def fit_and_predict(self):
        print("Starting fitting procedure...\n")
        model = svm.SVC(kernel='linear', C=1)
        X_all = self.DB['data']
        y_all = self.DB['target']
        X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.333, random_state=117)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        acc = model.score(X_test, y_test)    
        print("Accuracy %.3f" %acc)
        
        class_names = np.array([str(c) for c in self.DB['target_names']])
        print(classification_report(y_test, y_pred, labels=None, target_names=class_names, digits=3))

        # clf = OneClassSVM(gamma='auto').fit(X_all, y_all)
        # xnew1 = np.array([30, 1000, 31, 40, 8])
        # xnew2 = np.array([2.38723733e+00, 8.50546536e+01, 9.22250799e+00, 8.47817817e-01, 1.92842900e+00])
        # # xnew = xnew.reshape(1,-1)
        # xnew3 = np.array([-2.38575578e+00, 8.55363083e+01, 9.24858413e+00, 7.11980226e-01, 1.64921218e+00])
        # print(clf.predict([xnew1, xnew2, xnew3]))

        # ynew = model.predict(xnew)
        # print("ynew = " + str(ynew))
        print("Fitting procedure ended")


    def k_fold(self):
        print("Starting cross validation process with increasing number of splits...\n")
        model = svm.SVC(kernel='linear', C=1)
        X_all = self.DB['data']
        y_all = self.DB['target']
        for i in range(2, 16):
            print("Splits: " + str(i))
            cv = ShuffleSplit(n_splits=i, test_size=0.5, random_state=15)
            scores = cross_val_score(model, X_all, y_all, cv=cv)
            print(np.average(scores))
            print()
        
        print("Cross validation process ended")


    def seek_chunk_size(self):

        self.extract_simulation_data(0)
        os.chdir(self.model_directory)
        self.connect_to_Matlab()
        self.simulate()
        os.chdir(self.base_path)
        self.create_data_structures()
        self.extract_data()

        for size in range(5, 100, 5):    
            print("Seeking performances with chunk size: " + str(size))
            self.split_residuals(size, True)
            self.fit_and_predict()
            print()


    def seek_var(self, init_var, name1, name2, interval, increment, var_constant):
        i = 1
        var = init_var        

        self.set_spec_var(var_constant, var)
        self.simulate()
        self.extract_data()

        mse = 100 - my_stats.mse(self.csv_data[name1], self.csv_data[name2])

        print("Simulation number: " + str(i))
        print("Variance: " + str(var))
        print("MSE: " + str(mse))
        print()

        while (mse < interval[0] or mse > interval[1]):
            i += 1

            if (mse > interval[1]):
                var += increment
            else:
                var -= increment

            self.set_spec_var(var_constant, var)
            self.simulate()
            self.extract_data()

            mse = 100 - my_stats.mse(self.csv_data[name1], self.csv_data[name2])

            print("Simulation number: " + str(i))
            print("Variance: " + str(var))
            print("MSE: " + str(mse))
            print()

        return var


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
        # self.write_data()

        # plot values
        # self.plotAll()

        # calculate stats and save it in csv format file
        # self.residual_residual_stats()
        self.write_stats()

        self.split_residuals()

        self.fit_and_predict()

        self.k_fold()

        # DA RIVEDERE
        # calculate mse for speed and transmission
        # print("MSE for speed:")
        # print(100 - my_stats.mse(self.csv_data['speed'], self.csv_data['noisy_speed']))
        # print("MSE for transmissione speed;")
        # print(100 - my_stats.mse(self.csv_data['transmission'], self.csv_data['noisy_transmission']))
        # print()

        # print("Correlation:")
        # print(self.corr(self.csv_data))
        
        # end the simulation, then the program
        self.disconnect()


    def seek_var_car(self):

        self.extract_simulation_data(0)
        self.create_data_structures()
        os.chdir(self.model_directory)
        self.connect_to_Matlab()
        # [["transmission", "noisy_transmission", 500, 10, "transmission_var", [80, 90]], ["speed", "noisy_speed", 100, 2, "speed_var"], [90, 95]]
        for cup in self.variance_tuples:
            var = self.seek_var(cup[2], cup[0], cup[1], cup[5], cup[3], cup[4])
            print("BEST VARIANCE FOR " + cup[0] + ": " + str(var))
            print()

        os.chdir(self.base_path)


    def simulate_apollo(self, noisy):

        # extracts data needed to simulate the model
        self.extract_simulation_data(1)

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
        # self.write_data()

        # plot values
        # self.plotAll()

        # calculate stats and save it in csv format file
        # self.residual_residual_stats()
        self.write_stats()

        self.split_residuals()

        self.fit_and_predict()

        # DA RIVEDERE
        # calculate mse for speed and transmission
        # print("MSE for speed:")
        # print(100 - my_stats.mse(self.csv_data['speed'], self.csv_data['noisy_speed']))
        # print("MSE for transmissione speed;")
        # print(100 - my_stats.mse(self.csv_data['transmission'], self.csv_data['noisy_transmission']))
        # print()

        # print("Correlation:")
        # print(self.corr(self.csv_data))
        
        # end the simulation, then the program
        self.disconnect()


    def seek_var_apollo(self):
    
        self.extract_simulation_data(1)
        self.create_data_structures()
        os.chdir(self.model_directory)
        self.connect_to_Matlab()

        for cup in self.variance_tuples:
            var = self.seek_var(cup[2], cup[0], cup[1], cup[5], cup[3], cup[4])
            print("BEST VARIANCE FOR " + cup[0] + ": " + str(var))
            print()

        os.chdir(self.base_path)

# sm = SimulinkPlant('input.json')
# sm.simulate_car(False)