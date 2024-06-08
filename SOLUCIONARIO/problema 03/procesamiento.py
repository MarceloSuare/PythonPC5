import pandas as pd
import pymongo
import requests

def limpiar_columnas(df):
    # Renombrar columnas eliminando espacios, tildes y convirtiendo a minúsculas
    df.rename(columns=lambda x: x.strip().lower().replace(" ", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u"), inplace=True)
    
    # Eliminar columnas repetidas (ID y TipoMoneda)
    df = df.loc[:, ~df.columns.duplicated()]
    
    # Eliminar caracteres no deseados de la columna 'DISPOSITIVOLEGAL'
    df['dispositivolegal'] = df['dispositivolegal'].str.replace(',', '')
    
    return df

def obtener_tipo_cambio():
    # Aquí iría la lógica para obtener el tipo de cambio actual desde la API de Sunat
    tipo_cambio = 3.8  # Por ahora se usa un valor fijo como ejemplo
    return tipo_cambio

def dolarizar_montos(df):
    tipo_cambio = obtener_tipo_cambio()
    df['montodeinversiondolarizado'] = df['montodeinversion'] / tipo_cambio
    df['montodetransferenciadolarizado'] = df['montodetransferencia'] / tipo_cambio
    return df

def mapear_estado(estado):
    if estado == 'ActosPrevios':
        return 1
    elif estado == 'Resuelto':
        return 0
    elif estado == 'Ejecucion':
        return 2
    elif estado == 'Concluido':
        return 3

def puntuar_estado(df):
    df['puntuacionestado'] = df['estado'].apply(mapear_estado)
    return df

def subir_a_mongodb(df):
    # Código para subir la información a MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["mi_basededatos"]
    collection = db["mi_coleccion"]
    records = df.to_dict(orient='records')
    collection.insert_many(records)

def main():
    # Cargar el archivo Excel
    ruta_archivo = '/workspaces/PythonPC5/SOLUCIONARIO/data/reactiva.xlsx'
    df = pd.read_excel(ruta_archivo)

    # Limpiar columnas
    df = limpiar_columnas(df)

    # Subir información a MongoDB
    subir_a_mongodb(df)

    # Dolarizar montos
    df = dolarizar_montos(df)

    # Cambiar valores de la columna "Estado"
    df['estado'] = df['estado'].map({'Actos Previos': 'ActosPrevios', 'Concluido': 'Concluido', 'Resuelto': 'Resuelto', 'Ejecucion': 'Ejecución'})

    # Puntuar estado
    df = puntuar_estado(df)

    # Guardar el DataFrame modificado en un nuevo archivo Excel
    df.to_excel('/workspaces/PythonPC5/SOLUCIONARIO/reactiva_procesada.xlsx', index=False)

if __name__ == "__main__":
    main()
