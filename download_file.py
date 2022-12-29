# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 19:03:10 2022

@author: antos
"""
import os
import requests
import pyarrow as pa

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
            return open(self.percorsoFile, "wb").write(response.content)
        
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

        