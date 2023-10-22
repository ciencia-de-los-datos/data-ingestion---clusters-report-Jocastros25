"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""
import pandas as pd

def ingest_data():
    df = pd.read_fwf('clusters_report.txt', 
                     widths=[7,16,16,80], 
                     names=['Cluster', 'Cantidad de palabras clave', 'Porcentaje de palabras clave', 'Principales palabras clave'], 
                     skiprows=[0, 1, 2, 3],
                     skip_footer=True,
                     keep_default_na=False,
                     na_filter=True,
                     verbose=True,
                     warn_bad_lines=False
                     )
    
    for index, element in enumerate(df['Cluster']):
        if element == '':
            df.loc[index, 'Cluster'] = df.loc[index - 1, 'Cluster']
            df.loc[index, 'Cantidad de palabras clave'] = df.loc[index - 1, 'Cantidad de palabras clave']
            df.loc[index, 'Porcentaje de palabras clave'] = df.loc[index - 1, 'Porcentaje de palabras clave']

    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.lower()
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].str.replace("%", '').str.replace(",", '.').astype(float)

    for name in df.columns:
        df[name] = df[name].apply(lambda value: " ".join(str(value).strip().split()))

    df['cluster'] = df['cluster'].astype(int)
    df['cantidad_de_palabras_clave'] = df['cantidad_de_palabras_clave'].astype(int)
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].astype(float)

    df = df.groupby(['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave'])['principales_palabras_clave'].apply(' '.join).reset_index()

    for index, element in enumerate(df['principales_palabras_clave']):
        if element.endswith('.'):
            df.loc[index, 'principales_palabras_clave'] = element[:-1]

    return df
