# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 15:50:13 2022

@author: Claudia
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class Analisi_dati():
    
    """
     Analisi del file csv: calcolo del numero medio di viaggi al giorno rispetto all'intero mese
     Analizziamo la colonna relativa alle partenze dei taxi

    Returns
    -------
    None.
            
        
    """         
    
    def filtra_mese_corretto(self, dati_taxi, indcol:str, anno_mese:str):
        
        """
        Parameters
        ----------
        dati_taxi : dataFrame da filtrare
        indcol : string, indice della colonna con le date
        anno_mese : string, anno e mese di interese nel formato: YYYY-MM
        (Passiamo anno-mese per eliminare le date scorrette presenti nel dataFrame)
        
        Returns
        -------
        TYPE dati_taxi
            dataframe corretto (non contiene date errate e valori NaN)

        """
        #mesi sbagliati contiene gli indici delle date sbagliate del dataframe
        mesi_sbagliati=[]
        #a indice della colonna che vogliamo scorrere (colonna delle partenze); b valore all'interno della colonna. 
        for (a,b) in dati_taxi[indcol].items():
            #trasformo in stringa perchè i valori nel dataFrame sono di tipo dataType e i valori risultano poco comparabili
            b=str(b)
            #Prendiamo solo i primi 7 termini della stringa delle partenze (slice), perchè consideriamo solo la data 
            b=b[:7]
            if b != anno_mese:
                mesi_sbagliati.append(a)
                
        dati_taxi.drop(mesi_sbagliati,axis=0,inplace=True)
        return dati_taxi
        
        
    def filtra_dataFrame(self,dati_taxi,columns=list):
        """
        Parameters
        ----------
        dati_taxi: dataframe corretto
        columns:

        Returns
        -------
        TYPE dati_filtrati
        
        """
        dati_filtrati=dati_taxi[columns]
        return dati_filtrati

    
    def conta_occorrenze(self,series):
        """
        Parameters
        ----------
        Series: series contenente le date delle partenze

        Returns: 
            TYPE numero_corse_giornaliere
                
        """
        numero_corse_giornaliere={}
        for b in series:
            if str(b) in numero_corse_giornaliere.keys():
                numero_corse_giornaliere[str(b)]+=1
            else:
                numero_corse_giornaliere[str(b)]=1
        return numero_corse_giornaliere
    
    
    def borough_id_finder(self,series):
        
        """
        Parameters
        ----------
        Series: series contenente i borough
        
        Returns: 
            TYPE borough_id
            dizionario che ha come chiave il borough, e come valore le liste degli id delle zone associate al borough 
              
        """
        #mi salvo gli indici che compaiono in ogni borough in un dizionario
        borough_id={}
        for a,b in series.items(): #items mi restituisce ogni volta una tupla: a scorre gli indici e b il valore del borough della series
            if str(b) in borough_id.keys():
                borough_id[str(b)].append(a+1) #a+1 perchè l'indice è scalato di 1 rispeto alla locationID
            else:
                borough_id[str(b)]=[a+1]
        return borough_id
    
    
    def media_viaggi_mese(self,numero_corse_giornaliere):
        """
        Parameters
        ----------
        numero_corse_giornaliere: dizionario che contiene il numero di corse giornaliere per ogni mese

        Returns
        -------
        TYPE media 
             media del numero di corse al mese diviso il numero di giorni del mese
        
        """
        numero_corse_mese=0
        numero_giorni_mese=len(numero_corse_giornaliere.keys())
        numero_corse_mese = sum(numero_corse_giornaliere.values())
        media=numero_corse_mese/numero_giorni_mese
        return media

    def mese_con_media_maggiore(self, dict_media_corse_mese):
        """
        Parameters
        ----------
        dict_media_corse_mese = dizionario che contiene le medie associate ad ogni mese

        Returns
        -------
        TYPE  mese_con_media_maggiore
             il mese che ha la media più alta
        
        """
        mese_con_media_maggiore=0
        mese_con_media_maggiore=max(dict_media_corse_mese, key=dict_media_corse_mese.get)
        print("Il mese con la media maggiore fra quelli analizzati è ", mese_con_media_maggiore)
        return mese_con_media_maggiore


    
    def plot(self, media_corse_dF):
        """
        Parameters
        ----------
        media_corse_dF : dataframe contenente le medie associate ad ogni mese

        Returns
        -------
        TYPE None
            Istogramma che contiene sull'asse delle x i mesi e su quello delle y le medie associate
        """
       # plt.figure(figsize=(1, 90000))
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        dt_string = 'plotAnalisiDel'+dt_string + '.jpg'
        media_corse_dF.plot(x = 'Mese', y = 'Media', color = 'green', kind = 'bar')
        plt.title('Media corse al mese')
        plt.savefig(dt_string, bbox_inches='tight', dpi=1200)
        plt.show()
       # plt.close()
        return 
        
        
    def percentuale_viaggi_al_mese(self,numero_corse_giornaliere, numero_corse_mese):
        
        """
        Prende in ingresso:
            
            numero corse giornaliere 
        
        Returns:
        --------
        dizionario: media corse giornaliere
          è la media di viaggi effettuati in un determinato giorno rispetto ai viaggi del mese considerato 
             
        """
        
        #mi restituisce la media delle corse giornaliere per un unico mese 
        percentuale_corse_gionaliere={}
        for i in numero_corse_giornaliere.keys():
            percentuale_corse_gionaliere[i]=numero_corse_giornaliere[i]/numero_corse_mese #mi restituisce la media su ogni giorno del mese
        return percentuale_corse_gionaliere
    