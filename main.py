# -*- coding: utf-8 -*-
"""
In quale periodo dell'anno i taxi vengono utilizzati di più? Creare un file di risultati e
 un grafico che, per ogni mese, indichi il numero medio di viaggi registrati ogni giorno. 
 A causa delle differenze tra le zone di New York, vogliamo visualizzare le stesse 
 informazioni per ogni borough. Notate qualche differenza tra di loro? Qual è il mese con la media giornaliera
 più alta? E invece quello con la media giornaliera più bassa?
 
 """
import os
import time

import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt

from download_file import Download_file
from analisi_dati import Analisi_dati
from lettura_file import Leggi_file
from pdf import pdf

"""def generateCSV(mediaMaxNy, mediaMinNy, boroughAnalizzati, pathSaving):
    data = [[mediaMaxNy, mediaMinNy]]
    print(len(boroughAnalizzati))
    print(mediaMinNy)
    print(mediaMaxNy)
    
    for i in range(len(boroughAnalizzati)):
        
    header = ['Means Max Courses On NY', 'Means Min Courses On NY']

    with open(pathSaving + '/output.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(data)

    f.close()
    return "File Generato"""


def coverti_location_id(X, m=dict):
    """
    funzione aplicabile ad una series, che riconsce gli id delle location 
    presi dal csv e crea una series con i borough corrospondenti
    """
    for i in m.keys():
        for j in range(len(m[i])):
            if X == m[i][j]:
                X = i
                return X


# funzione che converte stringhe di data ed ora in timestamp
def converti_timestamp(X):
    ts = time.mktime(time.strptime(str(X), "%Y-%m-%d %H:%M:%S"))
    return ts


# funzione che restituisce solo la data da un stringa con data ed ora
def converti_solo_data(X):
    data = str(X).split(' ')
    return data[0]


if __name__ == '__main__':

    meseDaLeggere = input("Quali mesi vuoi analizzare? (formato input: anno-mese, diviso da spazi): ")
    meseDaLeggere = meseDaLeggere.split(' ')
    # split mi restituisce una lista di stringhe, cioè la lista di mesi che do in input
    # dati_filtrati= pd.DataFrame() #inizializzo dataFrame vuoto dei risultati
    boroughDaLeggere = input("Quali borough vuoi analizzare?\n -0 Bronx\n -1 Brooklyn\n -2 EWR\n"
                             " -3 Manhattan\n -4 Queens\n -5 Staten Island\n -6 Unknown\n "
                             "Inserire il valore corrispondente al borough da analizzare: ")
    boroughDaLeggere = boroughDaLeggere.split(' ')
    boroughList = ["Bronx", "Brooklyn", "EWR", "Manhattan", "Queens", "Staten Island", "Unknown"]
    numero_corse_giornaliere = {}
    dict_media_corse_mese = {}
    dict_numero_corse_giornaliere = {}
    dict_numero_corse_per_borough = {}
    dict_media_corse_per_borough = {}
    dict_percentuale_corse_giornaliere = {}
    dict_percentuale_corse_per_borough = {}
    media_corse_mese_borough = {}
    dict_borough_means = {}

    for mese_analizzato in range(len(meseDaLeggere)):  # scorro la lista dei mesi
        # scarico i file
        load = Download_file()
        load.check_or_download_file_parquet(meseDaLeggere[mese_analizzato])
        load.check_or_download_file_csv()

        lf = Leggi_file(meseDaLeggere[mese_analizzato])
        ad = Analisi_dati()
        dati_filtrati = pd.DataFrame()
        dati_taxi = lf.leggi_file_parquet()

        dati_taxi = ad.filtra_mese_corretto(dati_taxi, 'tpep_pickup_datetime', meseDaLeggere[mese_analizzato])
        #
        # prendo da prompt le colonne d'interesse separate da uno spazio
        # columns= (input('scrivere i gli indici delle colonne di interesse separate da uno spazio: '))
        # columns=columns.split(' ')
        # imposto e selezione le colonne del file che volgio analizzare
        zone_id = lf.leggi_file_csv()  # lettura csv: restituisce un dataFrame con gli id delle zone

        borough_id = ad.borough_id_finder(zone_id['Borough'])  # dizionario che associa id e borough

        columns = ["tpep_pickup_datetime", "tpep_dropoff_datetime", "PULocationID", "DOLocationID"]
        # richiama il metodo che filtra il dataframe

        for i in range(len(columns)):
            dati_filtrati[f'{columns[i]}_{meseDaLeggere[mese_analizzato]}'] = ad.filtra_dataFrame(dati_taxi, columns[i])

        # aggiungo un series al dataframe in cui le data delle partenze vengono sostituite da timestamp
        # dati_filtrati_jenuary["ts_pickup"]=dati_filtrati_jenuary['tpep_pickup_datetime'].apply(converti_timestamp)
        dati_filtrati[f'Pickup_Borough_{meseDaLeggere[mese_analizzato]}'] = dati_filtrati[
            f"PULocationID_{meseDaLeggere[mese_analizzato]}"].apply(coverti_location_id, m=borough_id)
        dati_filtrati[f"data_pickup_{meseDaLeggere[mese_analizzato]}"] = dati_filtrati[
            f'tpep_pickup_datetime_{meseDaLeggere[mese_analizzato]}'].apply(converti_solo_data)

        # Dizionario di dizionari: dizionario che associa ad ogni mese un dizionario che ha come chiave
        # la data del mese, e come valore il numero di corse in quella data
        numero_corse_giornaliere = ad.conta_occorrenze(dati_filtrati[f"data_pickup_{meseDaLeggere[mese_analizzato]}"])
        dict_numero_corse_giornaliere[f'{meseDaLeggere[mese_analizzato]}'] = numero_corse_giornaliere

        media_corse_mese = ad.media_viaggi_mese(numero_corse_giornaliere)
        dict_media_corse_mese[f'{meseDaLeggere[mese_analizzato]}'] = media_corse_mese

        # CALCOLO LE STESSE INFORMAZIONI PER BOROUGH
        numero_corse_per_borough = ad.conta_occorrenze(
            dati_filtrati[f"Pickup_Borough_{meseDaLeggere[mese_analizzato]}"])
        dict_numero_corse_per_borough[f'Corse_per_borough_{meseDaLeggere[mese_analizzato]}'] = numero_corse_per_borough

    # Per ogni mese, calcolo la media di viaggi dei borough
    # media_corse_per_borough = ad.media_viaggi_mese(numero_corse_per_borough)
    # dict_media_corse_per_borough[f'{meseDaLeggere[mese_analizzato]}']= media_corse_per_borough

    # agiunta per calcolo della media di corse mensili in quel determinato mese nel borough di partenza

    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    path = './outputFile/' + dt_string
    if (os.path.isdir(path) == False):
        os.makedirs(path)
    for i in range(len(boroughDaLeggere)):
        indice = int(boroughDaLeggere[i])
        media_corse_mese_borough[f"{boroughList[indice]}"] = {}
        for mese_analizzato in range(len(meseDaLeggere)):
            numeroCorse = dict_numero_corse_per_borough[f"Corse_per_borough_{meseDaLeggere[mese_analizzato]}"][
                f"{boroughList[indice]}"]
            media_corse_mese_borough[f"{boroughList[indice]}"][f"{meseDaLeggere[mese_analizzato]}"] = numeroCorse / len(
                dict_numero_corse_giornaliere[f"{meseDaLeggere[mese_analizzato]}"])
        borough = str(boroughList[indice])

        if borough not in dict_borough_means:
            dict_borough_means[f"{borough}"] = {}

        dict_borough_means[f"{borough}"]["meseConMediaMaggiore"] = max(media_corse_mese_borough[f"{boroughList[indice]}"])
        dict_borough_means[f"{borough}"]["valoreMediaMaggiore"] = str(max(media_corse_mese_borough[f"{boroughList[indice]}"].values()))
        dict_borough_means[f"{borough}"]["meseConMediaMinore"] = min(media_corse_mese_borough[f"{boroughList[indice]}"])
        dict_borough_means[f"{borough}"]["valoreMediaMinore"] = str(min(media_corse_mese_borough[f"{boroughList[indice]}"].values()))
        plt.title('Analisi del Borough: ' + borough)
        plt.bar(media_corse_mese_borough[f"{boroughList[indice]}"].keys(),
                media_corse_mese_borough[f"{boroughList[indice]}"].values(), color='green')
        plt.draw()
        plt.xticks(rotation=30, ha='right')
        plt.savefig(path + "/" + borough + ".jpg", bbox_inches='tight', dpi=1200)

    # Converto dizionario in dataFrame
    media_corse_dF = pd.DataFrame(dict_media_corse_mese.items(), columns=['Mese', 'Media'])

    # Calcolo il mese con la media maggiore
    mese_con_media_maggiore = ad.mese_con_media_maggiore(dict_media_corse_mese)
    mese_con_media_minore = ad.mese_con_media_minore(dict_media_corse_mese)

    # Plot: istogramma
    plot = ad.plot(media_corse_dF, dt_string)
    # csvGenerator = generateCSV(mese_con_media_maggiore, mese_con_media_minore[0], media_corse_mese_borough, path)

    # #Dizionario di dizionari: dizionario che associa ad ogni mese un dizionario che ha come chiave
    # #la data del mese, e come valore la media aritmetica delle corse giornaliere sulle corse dell'intero mese
    # percentuale_corse_gionaliere= ad.percentuale_viaggi_al_mese(numero_corse_giornaliere,numero_corse_mese)
    # dict_percentuale_corse_giornaliere[f'{meseDaLeggere[mese_analizzato]}']= percentuale_corse_gionaliere

    # #Calcolo dizionario con numero di corse medie per borough
    # percentuale_corse_per_borough = ad.percentuale_viaggi_al_mese(numero_corse_per_borough, numero_corse_mese)
    # dict_percentuale_corse_per_borough[f'Media_corse_borough_{meseDaLeggere[mese_analizzato]}']=percentuale_corse_per_borough
    # """

    pdf = pdf()
    meseDaLeggereString = ' '.join(meseDaLeggere)
    pdf.newFile(path, meseDaLeggereString, mese_con_media_maggiore, str(dict_media_corse_mese[mese_con_media_maggiore]),
                mese_con_media_minore[0], str(dict_media_corse_mese[mese_con_media_minore[0]]), dict_borough_means)
