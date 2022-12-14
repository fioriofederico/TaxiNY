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
    meseDaLeggere = input("che mese si vuole analizzare: ")
    if os.path.isdir(path) == False:
        os.makedirs(path)
    file=typeData+meseDaLeggere+extensionFile
    URL = ("https://d37ci6vzurychx.cloudfront.net/trip-data/")+file
    response = requests.get(URL)
    percorsoFile = path + file
    open(percorsoFile, "wb").write(response.content)
    fileCsv = ("taxi+_zone_lookup.csv")
    URLCsv = ("https://d37ci6vzurychx.cloudfront.net/misc/")+fileCsv
    response = requests.get(URLCsv)
    percorsoFileCsv = path+fileCsv
    open(percorsoFileCsv, "wb").write(response.content)
    isFile = os.path.isfile(percorsoFile)
    if isFile == True:
        dati_taxi=leggi_file.leggi_file_parquet(percorsoFile)
        
        dati_taxi=analisi_dati.filtra_mese_corretto(dati_taxi,'tpep_pickup_datetime',meseDaLeggere)
        #prendo da prompt le colonne d'interesse separate da uno spazio
        #columns= (input('scrivere i gli indici delle colonne di interesse separate da uno spazio: '))
        #columns=columns.split(' ')
        #imposto e selezione le colonne del file che volgio analizzare
        zone_id=leggi_file.leggi_file_csv('./inputFile/taxi+_zone_lookup.csv')
        borough_id=analisi_dati.borough_id_finder(zone_id['Borough'])
        
        columns =  ["tpep_pickup_datetime", "tpep_dropoff_datetime", "PULocationID", "DOLocationID"]
        #richiama il metodo che filtra il dataframe
        dati_filtrati_jenuary=analisi_dati.filtra_dataFrame(dati_taxi, columns)
        
        
        
        #aggiungo un series al dataframe in cui le data delle partenze vengono sostituite da timestamp
        #dati_filtrati_jenuary["ts_pickup"]=dati_filtrati_jenuary['tpep_pickup_datetime'].apply(converti_timestamp)
        dati_filtrati_jenuary['Pickup_Borough']=dati_filtrati_jenuary["PULocationID"].apply(coverti_location_id,m=borough_id)
        dati_filtrati_jenuary["data_pickup"]=dati_filtrati_jenuary['tpep_pickup_datetime'].apply(converti_solo_data)
        numero_corse_giornaliere=analisi_dati.numero_viaggi_al_giorno(dati_filtrati_jenuary["data_pickup"])
    else:
        print("File non presente verificare che il nominativo corrisponda al nome originale del file presente nel dossiet")