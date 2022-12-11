# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 15:50:13 2022

@author: Claudia
"""

import pandas as pd

class analisi_dati():
    """
    Calcolo numero medio di viaggi al giorno su ogni mese (verso ogni destinazione):
        numero totale dei viaggi ogni giorno diviso il numero dei viaggi totali del mese
        
        Considero la colonna che indica le date
        attraverso timestamp codifico le date in secondi
        ad esempio: 2022-01-01 in 00:00:00 corrisponde a 1640991600
        2022-02-01 in 00:00:00 corrisponde a 1643670000
        Quindi il mese di gennaio corrisponderà a tutti i valori compresi fra i due valori timestamp
            
        
    """
    
    def __init__(self):
        """
        Costruttore
        """
    def filtra_mese_corretto(dati_taxi,indcol=str,anno_mese=str):
        """
        

        Parameters
        
        ----------
        dati_taxi : dataFrame da filtrare
        indcol : string, indice della colonna con le date
        anno_mese : string, anno e mese di interese nel formato: YYYY-MM
        Returns
        -------
        dati_taxi : TYPE
            DESCRIPTION.

        """
        mesi_sbagliati=[]
        for (a,b) in dati_taxi[indcol].items():
            b=str(b)
            b=b[:7]
            if b != anno_mese:
                mesi_sbagliati.append(a)
                
        dati_taxi.drop(mesi_sbagliati,axis=0,inplace=True)
        return dati_taxi
        
        
        
    def filtra_dataFrame(dati_taxi,columns=list):
        dati_filtrati=dati_taxi[columns]
        return dati_filtrati
    
        
          
        
        
    def conversione_dati():
        """
        Restituisco colonna delle date del dataFrame codificata in timestamp
        
        """
        pass 
    
    def numero_viaggi_al_giorno(series):
        """
        Prende in ingresso i dati codificati da conversione_dati() e il giorno che voglio considerare
        Calcolo la somma del numero di viaggi effettuati nel giorno che viene richiesto nel main
        
        
        Returns: numeroViaggi 
              somma del numero di viaggi al giorno (per il giorno considerato) 
        """
        numero_corse_giornaliere={}
        for b in series:
            if str(b) in numero_corse_giornaliere.keys():
                numero_corse_giornaliere[str(b)]+=1
            else:
                numero_corse_giornaliere[str(b)]=1
        return numero_corse_giornaliere
    
    def numero_viaggi_al_mese():
        
        """
        Prende in ingresso:
            
            numeroViaggi
            mese 
             (mese su cui voglio calcolare la media )
             
        Calcolo:
            
        numGiorniMese
            = la somma del numero di giorni totali presenti nel mese (N.B. sono diversi in base al mese considerato, 
                                                                      possiamo fare un dizionario che contiene il numero 
                                                                      di giorni per ogni mese?)
        media = numeroViaggi / numGiorniMese
        
        Returns:
        --------
        media
          è la media di viaggi effettuati in un determinato giorno rispetto al mese considerato
             
        """
        
        pass 

