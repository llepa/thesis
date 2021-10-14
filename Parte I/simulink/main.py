import ml
import markov
import sys

def main():
    
	sm = ml.SimulinkPlant('input.json')
	if(sys.argv[1] == 'car'):
		sm.simulate_car()
	elif(sys.argv[1] == 'apollo'):
    		sm.simulate_apollo()

if __name__ == '__main__':
	main()
