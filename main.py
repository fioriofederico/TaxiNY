# -*- coding: utf-8 -*-
"""
In quale periodo dell'anno i taxi vengono utilizzati di più? Creare un file di risultati e
 un grafico che, per ogni mese, indichi il numero medio di viaggi registrati ogni giorno. 
 A causa delle differenze tra le zone di New York, vogliamo visualizzare le stesse 
 informazioni per ogni borough. Notate qualche differenza tra di loro? Qual è il mese 
 """
from lettura_file import leggi_file
from analisi_dati import analisi_dati
import os
import time
import requests
import pandas as pd

def coverti_location_id(X,m=dict):
    """
    funzione aplicabile ad una series, che riconsce gli id delle location 
    presi dal csv e crea una series con i borough corrospondenti
    """
    for i in m.keys():
        for j in range(len(m[i])):
            if X == m[i][j]:
                X=i
                return X
#funzione che converte stringhe di data ed ora in timestamp
def converti_timestamp(X):
    ts = time.mktime(time.strptime(str(X), "%Y-%m-%d %H:%M:%S"))
    return ts
#funzione che restituisce solo la data da un stringa con data ed ora 
def converti_solo_data(X):
    data=str(X).split(' ')
    return data[0]
    
if __name__=='__main__':
    path = ("./inputFile/")
    extensionFile = (".parquet")
    typeData = ("yellow_tripdata_")
    #percorsoFile = input("dammi il percoso del file da leggere: ")
    #assegno una lista al mese da leggere 
    meseDaLeggere =input(" Quali mesi vuoi analizzare? (formato input: anno-mese, diviso da spazi): ") 
    meseDaLeggere=meseDaLeggere.split(' ') #split mi restituisce una lista di stringhe, cioè la lista di mesi che do in input
    dati_filtrati= pd.DataFrame() #inizializzo dataFrame vuoto dei risultati 
    
    numero_corse_giornaliere={}
    dict_numero_corse_giornaliere={}
    for mese_analizzato in range(len(meseDaLeggere)): #scorro la lista dei mesi 
    #scarico i file
        if os.path.isdir(path) == False: 
            os.makedirs(path)
        file=typeData+meseDaLeggere[mese_analizzato]+extensionFile
        percorsoFile = path + file
        if os.path.isfile(percorsoFile) == False:
            URL = ("https://d37ci6vzurychx.cloudfront.net/trip-data/")+file
            response = requests.get(URL)
            open(percorsoFile, "wb").write(response.content)
        fileCsv = ("taxi+_zone_lookup.csv")
        if os.path.isfile(path+fileCsv) == False:
            URLCsv = ("https://d37ci6vzurychx.cloudfront.net/misc/")+fileCsv
            response = requests.get(URLCsv)
            percorsoFileCsv = path+fileCsv
            open(percorsoFileCsv, "wb").write(response.content) 
            
    
        dati_taxi = leggi_file.leggi_file_parquet(percorsoFile)
        dati_taxi = analisi_dati.filtra_mese_corretto(dati_taxi, 'tpep_pickup_datetime', meseDaLeggere[mese_analizzato])
        # prendo da prompt le colonne d'interesse separate da uno spazio
        # columns= (input('scrivere i gli indici delle colonne di interesse separate da uno spazio: '))
        # columns=columns.split(' ')
        # imposto e selezione le colonne del file che volgio analizzare
        zone_id = leggi_file.leggi_file_csv('./inputFile/taxi+_zone_lookup.csv') #lettura csv: restituisce un dataFrame con gli id delle zone
        borough_id = analisi_dati.borough_id_finder(zone_id['Borough']) #dizionario che associa id e borough
    
        columns = ["tpep_pickup_datetime", "tpep_dropoff_datetime", "PULocationID", "DOLocationID"] 
        # richiama il metodo che filtra il dataframe
        for i in range(len(columns)):
            dati_filtrati[f'{columns[i]}_{meseDaLeggere[mese_analizzato]}']= analisi_dati.filtra_dataFrame(dati_taxi, columns[i])
    
        # aggiungo un series al dataframe in cui le data delle partenze vengono sostituite da timestamp
        # dati_filtrati_jenuary["ts_pickup"]=dati_filtrati_jenuary['tpep_pickup_datetime'].apply(converti_timestamp)
        dati_filtrati[f'Pickup_Borough_{meseDaLeggere[mese_analizzato]}'] = dati_filtrati[f"PULocationID_{meseDaLeggere[mese_analizzato]}"].apply(coverti_location_id,m=borough_id)
        dati_filtrati[f"data_pickup_{meseDaLeggere[mese_analizzato]}"] = dati_filtrati[f'tpep_pickup_datetime_{meseDaLeggere[mese_analizzato]}'].apply(converti_solo_data)
        
        
        #Dizionario di dizionari: dizionario che associa ad ogni mese un dizionario che ha come chiave
        #la data del mese, e come valore il numero di corse in quella data
        numero_corse_giornaliere = analisi_dati.numero_viaggi_al_giorno(dati_filtrati[f"data_pickup_{meseDaLeggere[mese_analizzato]}"])
        dict_numero_corse_giornaliere[f'{meseDaLeggere[mese_analizzato]}']=numero_corse_giornaliere
        
        
        
        
        
      
        
       
        
        
        
        
        
        
        