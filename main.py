# -*- coding: utf-8 -*-


import pandas as pd 

dati_taxi=pd.read_parquet('yellow_tripdata_2022-01.parquet')

solo_data= dati_taxi['tpep_pickup_datetime']


dati_importanti=pd.DataFrame(dati_taxi,columns=['tpep_pickup_datetime', 'tpep_dropoff_datetime','PULocationID','DOLocationID'])
dati = dati_importanti.groupby('PULocationID')
print(dati)
