La cartella consegnata contiene al suo interno le due cartelle principali di questo progetto: _statistica_ e _simulink_.

La prima (_statistica_) contiene al suo interno il file stats.py che definisce tutte le funzioni riguardanti il calcolo dei momenti statistici del primo e del secondo ordine.

La seconda cartella (_simulink_) contiene al suo interno:

* _sim_, uno script bash che può essere lanciato da linea di comando per eseguire con più semplicità le simulazioni dei modelli; esso prende in input il nome del modello che si vuole simulare:
  * car - per avviare la simulazione del modello della macchina con cambio automatico;
  * apollo - per avviare la simulazione del modello dell'Apollo 11.
  
  (e.g. _./sim apollo_)

* _MATLAB_, la cartella che contiene i modelli Simulink/Matlab. Di seguito i modelli dei duei sistemi.

* _ml.py_, script python che carica tutte le librerie necessarie per poter interagire con Matlab e Simulink, si connette  con Matlab, carica il modello desiderato, esegue una simulazione del modello senza introduzione di rumore, e mostra l'output della simulazione attraverso un grafico. Gli stessi passaggi sono poi eseguiti introducendo rumore randomico nel sistema.

  Di seguito i grafici, senza introduzione di rumore e con introduzione di rumore dei due sistemi.

  _sf_car_using_duration.slx_
  
  <img width="1637" alt="Screenshot 2021-11-09 at 18 35 06" src="https://user-images.githubusercontent.com/51917777/140981572-eadf1da0-246f-4409-a3ec-696bb4707119.png">

  Prima dell'introduzione di rumore gaussiano
  <img width="962" alt="Screenshot 2021-11-09 at 17 30 45" src="https://user-images.githubusercontent.com/51917777/140964857-0283e14e-b627-431d-b21e-7e7fb20bd4bc.png">
  Dopo l'introduzione di rumore gaussiano (varianza 60 per la velocità e 2700 per la trasmissione)
  <img width="962" alt="Screenshot 2021-11-09 at 17 34 09" src="https://user-images.githubusercontent.com/51917777/140965447-c9fb6969-5273-401c-a2c9-af28697f692f.png">

  Di seguito i valori statistici, rispettivamente, per throttle, brake, speed, revs, gear, transmission.
  Prima dell'introduzione di rumore.
  <img width="1066" alt="Screenshot 2021-11-09 at 17 36 31" src="https://user-images.githubusercontent.com/51917777/140965870-47c91cff-8913-4b4c-9a6f-af4505197770.png">
  <img width="1066" alt="Screenshot 2021-11-09 at 17 37 22" src="https://user-images.githubusercontent.com/51917777/140966038-b908c38d-1146-45e9-bb41-70b37a5857ab.png">
  <img width="645" alt="Screenshot 2021-11-09 at 17 42 07" src="https://user-images.githubusercontent.com/51917777/140966829-3f0400cf-534a-4799-82bd-cc0e8c4be98f.png">

  Dopo l'introduzione di rumore.  
  <img width="1069" alt="Screenshot 2021-11-09 at 17 40 59" src="https://user-images.githubusercontent.com/51917777/140966595-dce7450f-e1a3-44dd-9322-755e64a25a93.png">
  <img width="1069" alt="Screenshot 2021-11-09 at 17 41 28" src="https://user-images.githubusercontent.com/51917777/140966687-e287914a-9fe1-4bd7-bf87-cf8ba6b77c4c.png">
  <img width="645" alt="Screenshot 2021-11-09 at 17 42 23" src="https://user-images.githubusercontent.com/51917777/140966864-9e4b8028-73dd-465e-b2c3-5452a4c87be8.png">

  _aero_dap3dof.slx_
  <img width="1333" alt="Screenshot 2021-11-09 at 17 56 45" src="https://user-images.githubusercontent.com/51917777/140970165-d7e512d5-af19-4ac9-aa25-b585f6cec09e.png">
  Prima di introdurre rumore gaussiano.
  (Attitude).
  <img width="886" alt="Screenshot 2021-11-09 at 18 12 28" src="https://user-images.githubusercontent.com/51917777/140972014-dcffb794-5bc9-41fd-832e-839eddbdb15e.png">
  
  Dopo l'introduzione di rumore guassiano (varianza 0.0000001).
  <img width="907" alt="Screenshot 2021-11-09 at 18 42 16" src="https://user-images.githubusercontent.com/51917777/140976469-d2dad7e4-4319-4a6b-9b00-a059c755c22c.png">

  Di seguito i valori statistici per yaw pitch e roll. 
  <img width="662" alt="Screenshot 2021-11-09 at 18 25 34" src="https://user-images.githubusercontent.com/51917777/140973973-57af62fa-a924-4925-846a-40faed4526c3.png">.
  
  E attitude (3 valori).
  
  <img width="617" alt="Screenshot 2021-11-09 at 18 38 09" src="https://user-images.githubusercontent.com/51917777/140975813-5ef34c5d-d2b8-4fb6-9c06-135bb6ba28e8.png">
  
  Dopo l'introduzione di rumore.
  (yaw, pitch, roll).
  
  <img width="642" alt="Screenshot 2021-11-09 at 18 46 38" src="https://user-images.githubusercontent.com/51917777/140977178-e988bc0b-5e5c-481e-8ed1-b858865e2edb.png">
  <img width="642" alt="Screenshot 2021-11-09 at 18 47 35" src="https://user-images.githubusercontent.com/51917777/140977162-1c01fa65-9e88-4a92-ac5b-7e9a1c13f2f9.png">
  
  (Attitude).
  
  <img width="642" alt="Screenshot 2021-11-09 at 19 15 31" src="https://user-images.githubusercontent.com/51917777/140981249-9bce5dcf-214a-4743-94ef-d43ea5cea315.png">

  
* _main.py_, script python che come punto di ingresso.

* input.json, file di configurazione json che descrive le informazioni necessarie per il caricamento dei modelli e i nomi delle variabli che contengono i dati che si vogliono visualizzare. 

* _markov.py_, script che rappresenta una catena di Markov, eventualmente da modificare, utilizzabile per introdurre rumore nel sistema. Non ancora utilizzata dal sistema.