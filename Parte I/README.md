La cartella consegnata contiene al suo interno le due cartelle principali di questo progetto: _statistica_ e _simulink_.

La prima (_statistica_) contiene al suo interno il file stats.py che definisce tutte le funzioni riguardanti il calcolo dei momenti statistici del primo e del secondo ordine.

La seconda cartella (_simulink_) contiene al suo interno:

* _sim_, uno script bash che può essere lanciato da linea di comando per eseguire con più semplicità le simulazioni dei modelli; esso prende in input il nome del modello che si vuole simulare:
  * car - per avviare la simulazione del modello della macchina con cambio automatico;
  * apollo - per avviare la simulazione del modello dell'Apollo 11.

* _MATLAB_, la cartella che contiene i modelli Simulink/Matlab. Di seguito i modelli dei duei sistemi.

* _ml.py_, script python che carica tutte le librerie necessarie per poter interagire con Matlab e Simulink, si connette  con Matlab, carica il modello desiderato, esegue una simulazione del modello senza introduzione di rumore, e mostra l'output della simulazione attraverso un grafico. Gli stessi passaggi sono poi eseguiti introducendo rumore randomico nel sistema.

  Di seguito i grafici, senza introduzione di rumore e con introduzione di rumore dei due sistemi.

  _sf_car_using_duration.slx_
  <img width="1575" alt="Screenshot 2021-10-15 at 15 19 28" src="https://user-images.githubusercontent.com/51917777/137493430-130a0949-228f-4b97-ac37-c1de00543233.png">

  _aero_dap3dof.slx_
  <img width="1575" alt="Screenshot 2021-10-15 at 15 25 16" src="https://user-images.githubusercontent.com/51917777/137494285-ad349315-619a-4e73-946b-dbb9c4d37aba.png">

* _main.py_, script python che come punto di ingresso.

* input.json, file di configurazione json che descrive le informazioni necessarie per il caricamento dei modelli e i nomi delle variabli che contengono i dati che si vogliono visualizzare. 
