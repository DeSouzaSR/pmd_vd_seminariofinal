#-------------------------------------------------------------------------------
# Name:        integra_mapa.py
# Purpose:
#   Integrar aos dados do município do IBGE, os dados pedagógicos.
# Author:      Sandro Ricardo De Souza
#
# Created:     05/06/2025
# Licence:     MIT
#-------------------------------------------------------------------------------

# Imports
import pandas as pd
import geopandas as gpd
pd.set_option('display.max_columns', None)

# Leitura de dados
df_geo = gpd.read_file(r'../data/raw_data/ES_Municipios_2024/ES_Municipios_2024.shp')
df_ped = pd.read_csv(r'../data/raw_data/df_es_filtrado.csv')

df_ped['ID_MUNICIPIO'] = df_ped['ID_MUNICIPIO'].astype('str')

# Inclusão das geometrias nos dados pedagógicos
#df_ped = df_ped.merge(df_geo, left_on='ID_MUNICIPIO', right_on='CD_MUN', how='left')

print(df_geo['CD_MUN'].unique())
print(df_ped['ID_MUNICIPIO'].unique())
