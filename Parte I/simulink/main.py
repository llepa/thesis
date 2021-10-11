import ml
import markov
import matlab.engine

def main():

	# import the json configuration file 
	sm = ml.SimulinkPlant('input.json')

	# load matlab and load the desired model 
	sm.connectToMatlab()

	# set the value of error: true if intended to introduce error in the system, false otherwise
	error = False

	# run the simulation
	sm.simulate(error)

	# end the simulation, then the program
	sm.disconnect()

if __name__ == '__main__':
	main()
