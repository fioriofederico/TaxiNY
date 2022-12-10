# -*- coding: utf-8 -*-
"""
@author: Claudia
"""

import pandas as pd 

class leggi_file():
    """
    lettura di un file generico
    """
    
    def __init__(self, percorsoFile=str):
        
        """
        Costruttore
        
        Parameters
        ----------
        percorsoFile = string 
           stringa che contiene il percorso del file da leggere
           
        Returns
        -------
        None.
        """
        
        self.percorsoFile = percorsoFile
        
        
    def leggi_file_parquet(percorsoFile):
        
        """
        Lettura dei file in formato .parquet

        Parameters
        ----------
        percorsoFile: string

        Returns
        -------
        dataFrame
        """
        try:
            dati_taxi=pd.read_parquet(percorsoFile, engine='pyarrow')
            return dati_taxi
        except:
            print("il file non è in formato .parquet")
    
    def leggi_file_csv(percorsoFile):
        """
        Lettura dei file in formato .csv
        
        Parameters
        ----------
        percorsoFile: string

        Returns
        -------
        dataFrame
        """
        try:
            dati_taxi = pd.read_csv(percorsoFile)
            return dati_taxi
        except:
            print("il file non è in formato .csv")

    
    def leggi_file_json(percorsoFile):
        """
        Lettura dei file in formato .json
        Parameters
        ----------
        percorsoFile: string

        Returns
        -------
        dataFrame
        """
        try:
            dati_taxi= pd.read_json(percorsoFile)
            return dati_taxi
        except:
            print("il file non è in formato .json")
            
    def leggi_file_txt(percorsoFile):
        """
        Lettura dei file in formato .txt
        Il carattere ";" viene utilizzato come separatore dei dati 
        
        Parameters
        ----------
        percorsoFile: string

        Returns
        -------
        dataFrame
        """
        dati_taxi= pd.read_csv(percorsoFile, sep= ";")
        return dati_taxi
    


    
