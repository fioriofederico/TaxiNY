# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 15:50:13 2022

@author: Claudia
"""

import pandas as pd
import matplotlib.pyplot as plt 

class Analisi_dati():
    """
    Calcolo numero medio di viaggi al giorno su ogni mese (verso ogni destinazione):
        numero totale dei viaggi ogni giorno diviso il numero dei viaggi totali del mese
        
        Considero la colonna che indica le date
        attraverso timestamp codifico le date in secondi
        ad esempio: 2022-01-01 in 00:00:00 corrisponde a 1640991600
        2022-02-01 in 00:00:00 corrisponde a 1643670000
        Quindi il mese di gennaio corrisponderà a tutti i valori compresi fra i due valori timestamp
            
        
    """
    
    def filtra_mese_corretto(self,dati_taxi, indcol:str, anno_mese:str):
        """
        Parameters
        ----------
        dati_taxi : dataFrame da filtrare
        indcol : string, indice della colonna con le date
        anno_mese : string, anno e mese di interese nel formato: YYYY-MM
        (Passiamo anno-mese per eliminare le date scorrette presenti nel dataFrame)
        Returns
        -------
        dati_taxi : TYPE
            DESCRIPTION.

        """
        #mesi sbagliati contiene gli indici delle date sbagliate del dataframe
        mesi_sbagliati=[]
        #a indice, b valore all'interno della colonna. Il ciclo scorre la colonna di cui specifichiamo l'indice
        #(noi consideriamo sempre quello delle partenze)
        for (a,b) in dati_taxi[indcol].items():
            #trasformo in stringa perchè i valori nel dataFrame sono di tipo dataType e i valori risultano poco comparabili
            b=str(b)
            #la stringa delle partenze contiene sia data che ora. A noi serve solo la data, quindi faccio lo slice: 
                #prendo solo i primi 7 termini della stringa
            b=b[:7]
            if b != anno_mese:
                mesi_sbagliati.append(a)
                
        dati_taxi.drop(mesi_sbagliati,axis=0,inplace=True)
        return dati_taxi
        
        
        
    def filtra_dataFrame(self,dati_taxi,columns=list):
        dati_filtrati=dati_taxi[columns]
        return dati_filtrati

    
    def conta_occorrenze(self,series):
        """
        
        Prende in ingresso una series (date delle partenze)
        Lo uso per calcolare: 
            numero_viaggi_al giorno
            numero_viaggi_per_borough
        
        
        Returns: 
            numero_corse_giornaliere
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
        Prende in ingresso la series con i borough
        
        Returns: dizionario che ha come chiave i borough e come valore le liste degli id delle zone associate al borough 
              
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
        #Sommo il numero di corse giornaliere
        numero_corse_mese=0
        media=float
        numero_giorni_mese=len(numero_corse_giornaliere.keys())
        numero_corse_mese = sum(numero_corse_giornaliere.values())
        media=numero_corse_mese/numero_giorni_mese
        return media
               
    def mese_con_media_maggiore(self, dict_media_corse_mese):
        mese_con_media_maggiore=0
        mese_con_media_maggiore=max(dict_media_corse_mese, key=dict_media_corse_mese.get)
        print("Il mese con la media maggiore fra quelli analizzati è ", mese_con_media_maggiore)
        return mese_con_media_maggiore
    
    def plot(self, media_corse_dF):
        media_corse_dF.plot(x = 'Mese', y = 'Media', color = 'green', kind = 'bar')
        plt.title('Media corse al mese')
        return plt.show()
        
        
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
        
    
    
    
    
    
    
    