#-------------------------------------------------------------------------------
# Name:        Explorar
# Purpose:
#
# Author:      srsouza
#
# Created:     04/06/2025
# Copyright:   (c) srsouza 2025
# Licence:     MIT
#-------------------------------------------------------------------------------

import pandas as pd
pd.set_option('display.max_columns', None)

path_pedagogico = r'../data/raw_data/df_es_filtrado.csv'
df_ped = pd.read_csv(path_pedagogico)


print(df_ped.head())

print("\nCódigos de municípios")
print(df_ped['ID_MUNICIPIO'].unique())

print('\nQuantidade de municípios')
print(len(df_ped['ID_MUNICIPIO'].unique()))