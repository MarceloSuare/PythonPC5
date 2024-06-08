import pandas as pd

# Cargar datos
df_airbnb = pd.read_csv("/workspaces/PythonPC5/SOLUCIONARIO/data/airbnb.csv")

# Caso 1: Búsqueda de alojamiento para Alicia
def buscar_alojamiento_alicia(df):
    df_filtrado = df[
        (df['accommodates'] >= 4) &
        (df['reviews'] > 10) &
        (df['overall_satisfaction'] > 4)
    ]
    df_ordenado = df_filtrado.sort_values(by=['overall_satisfaction', 'reviews'], ascending=[False, False])
    return df_ordenado.head(3)

alojamiento_alicia = buscar_alojamiento_alicia(df_airbnb)
print("Alojamientos para Alicia:")
print(alojamiento_alicia)

# Caso 2: Comparación de críticas entre Roberto y Clara
def comparar_criticas_roberto_clara(df):
    df_criticas = df[df['room_id'].isin([97503, 90387])]
    df_criticas.to_excel("roberto.xlsx", index=False)  # Cambiado a .xlsx
    return df_criticas

criticas_roberto_clara = comparar_criticas_roberto_clara(df_airbnb)
print("Críticas de Roberto y Clara:")
print(criticas_roberto_clara)

# Caso 3: Búsqueda de alojamiento para Diana
def buscar_alojamiento_diana(df):
    df_filtrado = df[
        (df['price'] <= 50) &
        (df['room_type'] == 'Shared room')
    ]
    df_ordenado = df_filtrado.sort_values(by=['overall_satisfaction'], ascending=False)
    return df_ordenado.head(10)

alojamiento_diana = buscar_alojamiento_diana(df_airbnb)
print("Alojamientos para Diana:")
print(alojamiento_diana)
