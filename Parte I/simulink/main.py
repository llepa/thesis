import ml
import throttle
import matlab.engine

def main():

	sm = ml.SimulinkPlant('input.json')
	sm.connectToMatlab()
	error = True
	sm.simulate(error)
	sm.outValues
	sm.simulate(False)
	sm.outValues
	
	sm.disconnect()
	

	#print()
	#print(sm.out)

if __name__ == '__main__':
	main()
