import ml
import sys

def main():
	
	sm = ml.SimulinkPlant('input.json')

	if (sys.argv[1] == 'car'):
			if(sys.argv[2] == 'noise'):
				sm.simulate_car(True)
			elif (sys.argv[2] == 'nonoise'):
					sm.simulate_car(False)
	elif (sys.argv[1] == 'apollo'):
			if (sys.argv[2] == 'noise'):
				sm.simulate_apollo(True)
			elif (sys.argv[2] == 'nonoise'):
					sm.simulate_apollo(False)

if __name__ == '__main__':
	main()
