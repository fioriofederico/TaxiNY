# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 19:03:10 2022

@author: antos
"""
import os
import requests
import matplotlib.pyplot as plt
from datetime import datetime

class Download_file:
     
    def __init__(self):
        self.path = ("./inputFile/")
        self.extensionFile = (".parquet")
        self.typeData = ("yellow_tripdata_")
        
    
    def check_or_download_file_parquet(self, meseDaLeggere: str):
        """

        Parameters
        ----------
        meseDaLeggere : str
            il mese del file da scaricare

        Returns 
        -------
        Se il file non è già stato scaricato, allora crea un a cartella inputFile
        e ci scarican il file all'inteno

        """
        file = self.typeData + meseDaLeggere + self.extensionFile
        percorsoFile = self.path + file
        if os.path.isdir(self.path) == False:
            os.makedirs(self.path)
        if os.path.isfile(percorsoFile) == False:
            URL = ("https://d37ci6vzurychx.cloudfront.net/trip-data/") + file
            response = requests.get(URL)
            return open(percorsoFile, "wb").write(response.content)
        
        
    def check_or_download_file_csv(self):
        """
        
        Returns
        -------
        Controlla che il fle Csv da scaricicare non sia nella cartella inputFile, altrimenti 
        lo scarica nella cartella 

        """
        fileCsv = ("taxi+_zone_lookup.csv")
        if os.path.isfile(self.path + fileCsv) == False:
            URLCsv = ("https://d37ci6vzurychx.cloudfront.net/misc/") + fileCsv
            response = requests.get(URLCsv)
            percorsoFileCsv = self.path + fileCsv
            return open(percorsoFileCsv, "wb").write(response.content)

    def create_outputfile(self, dict_numero_corse_giornaliere: dict, dict_numero_corse_per_borough: dict, media_corse_mese_borough: dict,boroughDaLeggere: list, meseDaLeggere: list):
        
        """
        
        Crea una cartella di output, il cui nome è costituito da data e l'ora in cui è stata svolta l'analisi, 
        che contiene i plot e i risultati
        
        Parameters
        ----------
        dict_numero_corse_giornaliere : dict
        dict_numero_corse_per_borough: dict
        media_corse_mese_borough: dict
        boroughDaLeggere: list
        meseDaLeggere: list
        

        Returns 
        -------
        dt_string : nome della cartella
        path : path della cartella creata
        dict_borough_means: un dizionario in cui vengono messi i valori di media maggiore e minore
                            per lo specifico borough
        
        """
        
        boroughList = ["Bronx", "Brooklyn", "EWR", "Manhattan", "Queens", "Staten Island", "Unknown"]
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        path = './outputFile/' + dt_string
        dict_borough_means = {}
        if (os.path.isdir(path) == False):
            os.makedirs(path)
        for i in range(len(boroughDaLeggere)):
            indice = int(boroughDaLeggere[i])
            media_corse_mese_borough[f"{boroughList[indice]}"] = {}
            for mese_analizzato in range(len(meseDaLeggere)):
                numeroCorse = dict_numero_corse_per_borough[f"Corse_per_borough_{meseDaLeggere[mese_analizzato]}"][f"{boroughList[indice]}"]
                    
                media_corse_mese_borough[f"{boroughList[indice]}"][f"{meseDaLeggere[mese_analizzato]}"] = numeroCorse / len(dict_numero_corse_giornaliere[f"{meseDaLeggere[mese_analizzato]}"])
                    
            borough = str(boroughList[indice])

            if borough not in dict_borough_means:
                dict_borough_means[f"{borough}"] = {}
            dict_borough_means[f"{borough}"]["valoreMediaMaggiore"] = str(
                max(media_corse_mese_borough[f"{boroughList[indice]}"].values()))
            dict_borough_means[f"{borough}"]["valoreMediaMinore"] = str(
                min(media_corse_mese_borough[f"{boroughList[indice]}"].values()))
            plt.title('Analisi del Borough: ' + borough)
            plt.bar(media_corse_mese_borough[f"{boroughList[indice]}"].keys(),
                    media_corse_mese_borough[f"{boroughList[indice]}"].values(), color='green')
            plt.draw()
            plt.xticks(rotation=30, ha='right')
            plt.savefig(path + "/" + borough + ".jpg", bbox_inches='tight', dpi=1200)
            plt.show()
        return dt_string, path, dict_borough_means
         