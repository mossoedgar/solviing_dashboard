import numpy as np
import pandas as pd
from sqlFunctions import queryTable


def create_df():
    query = '''
        SELECT
        *
        FROM precios_promedio_dashboard
    '''
    df = queryTable(query)

    df_filt = df[['entidad_federativa', 'municipio']]
    df_test = df_filt.groupby(['entidad_federativa','municipio']).count().reset_index()
    options_dict = df_test.groupby('entidad_federativa')['municipio'].agg(list).to_dict()

    return df, options_dict


def cleanFigureData(df):

    df['fecha'] = df['fecha'].astype(str)
    df['fecha'] = [x[:4] + ' ' + x[4:] for x in df['fecha']]

    if 'clave_entidad_federativa' in df.columns:
        df = df[~df['clave_entidad_federativa'].isna()]
        df['clave_entidad_federativa'] = df['clave_entidad_federativa'].astype(str)
        df = df[pd.to_numeric(df['clave_entidad_federativa'], errors='coerce').notnull()]
        #df = df.loc[df.SUPERFICIE_VENDIBLE.str.isnumeric()]
        df['clave_entidad_federativa'] = df['clave_entidad_federativa'].astype(int)
    if 'clave_municipio' in df.columns:
        df = df[~df['clave_municipio'].isna()]
        df['clave_municipio'] = df['clave_municipio'].astype(str)
        df = df[pd.to_numeric(df['clave_municipio'], errors='coerce').notnull()]
        #df = df.loc[df.SUPERFICIE_VENDIBLE.str.isnumeric()]
        df['clave_municipio'] = df['clave_municipio'].astype(int)
    
    if 'valor_mun_total_promedio' in df.columns:
        df['valor_mun_total_promedio'] = df['valor_mun_total_promedio'].astype(float)
        df['valor_mun_total_promedio'] = df['valor_mun_total_promedio'].round(2)

    if 'valor_mun_m2_promedio' in df.columns:
        df['valor_mun_m2_promedio'] = df['valor_mun_m2_promedio'].astype(float)
        df['valor_mun_m2_promedio'] = df['valor_mun_m2_promedio'].round(2)

    return df
