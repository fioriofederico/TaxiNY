# -*- coding: utf-8 -*-
"""
In quale periodo dell'anno i taxi vengono utilizzati di più? Creare un file di risultati
 e un grafico che, per ogni mese, indichi il numero medio di viaggi registrati ogni giorno.
 A causa delle differenze tra le zone di New York, vogliamo visualizzare le stesse informazioni
 per ogni borough. Notate qualche differenza tra di loro? Qual è il mese con la media giornaliera più alta?
 E invece quello con la media giornaliera più bassa?
"""

import pandas as pd 

class leggi_file():
    """
    lettura di un file generico
    """
    
    def __init__(self, percorsoFile=str):
        
        """
        Costruttore
        """
        
        self.percorsoFile = percorsoFile
        
    def leggi_file_parquet(percorsoFile):
        
        """
        Lettura dei file in formato .parquet
        """
        try:
            dati_taxi=pd.read_parquet(percorsoFile, engine='pyarrow')
            return dati_taxi
        except:
            print("il file non è in formato .parquet")
    
    def leggi_file_csv(percorsoFile):
        """
        Lettura dei file in formato .csv
        """
        try:
            dati_taxi = pd.read_csv(percorsoFile)
            return dati_taxi
        except:
            print("il file non è in formato csv")

    
    def leggi_file_json(percorsoFile):
        """
        Lettura dei file in formato .json
        """
        try:
            dati_taxi= pd.read_json(percorsoFile)
            return dati_taxi
        except:
            print("il file non è in formato json")
            
    def leggi_file_txt(percorsoFile):
        """
        Lettura dei file in formato .txt
        Il carattere ";" viene utilizzato come separatore dei dati 
        """
        dati_taxi= pd.read_csv(percorsoFile, sep= ";")
        return dati_taxi
    
    
    
    
    
    
    
    
    
    
    


#numero medio di viaggi registrati ogni giorno

#5 classi:
    #lettura (lettura csv, parquet, lettura dati input (richiesta tramite main))
    #analisi (conversione delle date o split, raggruppamento per corse, calcolo di un numero totale di corse giornaliere e media sul mese)
    #creo dataframe, e ogni id lo sostiuisco con la scritta della zona. Assegno a partenza e destinazione un numero identificativo.
    #creazione file csv di output.
    
#numero di corse con destinazione in un determinato posto. 


    
