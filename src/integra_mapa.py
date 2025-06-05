#-------------------------------------------------------------------------------
# Name:        integra_mapa.py
# Purpose:
#   Integrar aos dados do município do IBGE, os dados pedagógicos.
# Author:      Sandro Ricardo De Souza
#
# Created:     05/06/2025
# Licence:     MIT
#-------------------------------------------------------------------------------

import pandas as pd
import geopandas as gpd

dados_geo = gpd.read_file(r'../data/raw_data/ES_Municipios_2024/ES_Municipios_2024.shp')

print(dados_geo.head())