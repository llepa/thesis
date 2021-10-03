import ml
import throttle
import matlab.engine

def main():

	sm = ml.SimulinkPlant('sf_car_using_duration', './MATLAB/Examples/R2021a/stateflow/AutomaticTransmissionUsingDurationOperatorExample/sf_car_using_duration', ['vspeed.signals.values', 'revs.signals.values', 'gear.signals.values'], 'vspeed.time')
	sm.connectToMatlab()
	sm.simulate()
	
	sm.disconnect()
	

	#print()
	#print(sm.out)

if __name__ == '__main__':
	main()
