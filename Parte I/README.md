La cartella consegnata contiene al suo interno le due cartelle principali di questo progetto: _statistica_ e _simulink_.

La prima (_statistica_) contiene al suo interno il file stats.py che definisce tutte le funzioni riguardanti il calcolo dei momenti statistici del primo e del secondo ordine.

La seconda cartella (_simulink_) contiene al suo interno:

* _sim_, uno script bash che può essere lanciato da linea di comando per eseguire con più semplicità le simulazioni dei modelli; esso prende in input il nome del modello che si vuole simulare:
** car - per avviare la simulazione del modello della macchina con cambio automatico;
** apollo - per avviare la simulazione del modello dell'Apollo 11.

* _MATLAB_, la cartella che contiene i modelli Simulink/Matlab.
* _ml.py_, script python che carica tutte le librerie necessarie per poter interagire con Matlab e Simulink, si connette con Matlab, carica il modello desiderato, esegue una simulazione del modello senza introduzione di rumore, e mostra l'output della simulazione attraverso un grafico. Gli stessi passaggi sono poi eseguiti introducendo rumore nel sistema.
