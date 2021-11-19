import ml
import sys

def main():
    
    sm = ml.SimulinkPlant('input.json')

    if (sys.argv[1] == 'car'):
            if(sys.argv[2] == 'noise'):
                sm.simulate_car(True)
            elif (sys.argv[2] == 'nonoise'):
                    sm.simulate_car(False)
            elif (sys.argv[2] == 'variance'):
                    sm.seek_var_car()
            elif (sys.argv[2] == 'chunk'):
                    sm.seek_chunk_size(0)
                    
    elif (sys.argv[1] == 'apollo'):
            if (sys.argv[2] == 'noise'):
                sm.simulate_apollo(True)
            elif (sys.argv[2] == 'nonoise'):
                    sm.simulate_apollo(False)
            elif (sys.argv[2] == 'variance'):
                    sm.seek_var_apollo()
            elif (sys.argv[2] == 'chunk'):
                    sm.seek_chunk_size(1)
    
    elif (sys.argv[1] == 'climate'):
            if (sys.argv[2] == 'noise'):
                    sm.simulate_climate(True)
            elif (sys.argv[2] == 'nonoise'):
                    sm.simulate_climate(False)
            elif (sys.argv[2] == 'variance'):
                    sm.seek_var_climate()
            elif (sys.argv[2] == 'chunk'):
                    sm.seek_chunk_size(2)

if __name__ == '__main__':
    main()
